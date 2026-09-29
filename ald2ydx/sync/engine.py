"""Оркестратор синхронизации ALD Pro -> Яндекс 360.

Конвейер одного прохода:

1. Чтение поддерева подразделений ALD Pro из baseDN (метод 7.9, рекурсивный BFS).
2. Синхронизация структуры в Яндекс 360:
   - созданиеDepartmentService_Create (externalId = DN);
   - переименование/перемещение — DepartmentService_Update (name/parentId);
   - удаление — DepartmentService_Delete (если разрешено конфигом), обход снизу вверх.
3. Чтение сотрудников по подразделениям (7.21) + карточки (8.4) + proxyAddresses (8.19).
4. Синхронизация сотрудников:
   - создание — UserService_Create (externalId = login);
   - изменение ФИО/должности/контактов/перемещение между подразделениями — UserService_Update;
   - блокировка/разблокировка — UserService_Update (isEnabled);
   - удаление в источнике — UserService_Update (isEnabled=false и/или isDismissed=true),
     т.к. метода удаления сотрудника в API Яндекс 360 нет (см. README, раздел «Ограничения»).
5. Сохранение состояния (контрольная точка + снимок дерева) для инкрементальных прогонов.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from ..ald_pro.client import AldProClient, AldProError
from ..logging_setup import get_logger
from ..settings import Settings
from ..yandex360.client import Yandex360Client, Yandex360Error
from .mapping import (
    SyncState,
    build_contacts,
    normalize_dn,
    pick_email,
    to_nickname,
    utcnow_iso,
)

log = get_logger("sync")


@dataclass
class SyncReport:
    created_departments: int = 0
    updated_departments: int = 0
    deleted_departments: int = 0
    created_users: int = 0
    updated_users: int = 0
    blocked_users: int = 0
    unblocked_users: int = 0
    dismissed_users: int = 0
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "created_departments": self.created_departments,
            "updated_departments": self.updated_departments,
            "deleted_departments": self.deleted_departments,
            "created_users": self.created_users,
            "updated_users": self.updated_users,
            "blocked_users": self.blocked_users,
            "unblocked_users": self.unblocked_users,
            "dismissed_users": self.dismissed_users,
            "errors": self.errors,
        }


class DirectorySynchronizer:
    def __init__(self, settings: Settings, ald: AldProClient, ydx: Yandex360Client) -> None:
        self.cfg = settings
        self.ald = ald
        self.ydx = ydx
        self.report = SyncReport()
        self.state = SyncState.load(settings.sync.state_path)
        #: normalized ALD DN -> yandex departmentId
        self.dept_by_dn: dict[str, int] = {}
        #: yandex departmentId -> dept object
        self.dept_by_id: dict[int, dict[str, Any]] = {}
        #: externalId(login) -> user id
        self.user_by_extid: dict[str, str] = {}
        #: nickname -> user id
        self.user_by_nick: dict[str, str] = {}
        #: org email domain (для генерации email при отсутствии в ALD Pro)
        self.mail_domain = os.environ.get("A2Y_MAIL_DOMAIN", "")

    # ------------------------------------------------------------ utilities
    def _error(self, what: str, exc: Exception) -> None:
        msg = f"{what}: {exc}"
        log.error(msg)
        self.report.errors.append(msg)

    # ------------------------------------------------------- step: read ALD
    def read_ald_departments(self) -> list[dict[str, Any]]:
        """Читает всё поддерево OU из baseDN (ALD Pro 7.9) и детали (7.6)."""
        base_dn = self.cfg.sync.base_dn
        nodes = list(self.ald.walk_subtree(base_dn))
        log.info("ALD Pro: поддерево от %s содержит %d подразделений", base_dn, len(nodes))
        # сортируем по глубине DN — родители раньше детей
        nodes.sort(key=lambda n: n["dn"].count(","))
        for node in nodes:
            details = self.ald.get_ou_params(node["dn"])
            node["description"] = details.get("organizationunit_description") or ""
            node["manager_dn"] = details.get("organizationunit_manager_dn") or ""
        return nodes

    def read_ald_users(self, departments: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        """Собирает пользователей по всем подразделениям поддерева (7.21), карточки — 8.4.

        Возвращает: login -> {"list_item":..., "full": {...}, "proxy": [...]}.
        baseDN-подразделение также опрашивается на прямых пользователей.
        """
        scope_dns = [self.cfg.sync.base_dn] + [d["dn"] for d in departments]
        users: dict[str, dict[str, Any]] = {}
        for dn in scope_dns:
            for item in self.ald.iter_users_of_ou(dn):
                login = item.get("userlistitem_login")
                if not login or login in users:
                    continue
                users[login] = {"list_item": item}
        log.info("ALD Pro: найдено %d уникальных пользователей в поддереве", len(users))
        return users

    # ------------------------------------------------- step: sync departments
    def index_yandex_departments(self) -> None:
        """DepartmentService_List -> индексы externalId->id и id->объект."""
        for dept in self.ydx.list_departments():
            self.dept_by_id[int(dept["id"])] = dept
            ext = dept.get("externalId") or dept.get("external_id")
            if ext:
                self.dept_by_dn[normalize_dn(ext)] = int(dept["id"])
        log.info("Яндекс 360: проиндексировано %d подразделений", len(self.dept_by_id))

    def sync_departments(self, nodes: list[dict[str, Any]]) -> None:
        """Создание/обновление/удаление подразделений. Родители обрабатываются раньше детей."""
        current = {normalize_dn(n["dn"]) for n in nodes}
        dry = self.cfg.sync.dry_run

        for node in nodes:
            dn_key = normalize_dn(node["dn"])
            parent_key = normalize_dn(node["parent_dn"])
            # родитель либо корень синхронизации (root_department_id), либо уже созданный узел
            if parent_key == normalize_dn(self.cfg.sync.base_dn):
                parent_id = self.cfg.sync.root_department_id
            else:
                parent_id = self.dept_by_dn.get(parent_key)
            if parent_id is None:
                self._error(f"Подразделение {node['dn']}", RuntimeError("родитель ещё не синхронизирован"))
                continue

            try:
                existing_id = self.dept_by_dn.get(dn_key)
                if existing_id is None:
                    if dry:
                        log.info("[dry-run] CREATE dept name=%r parent=%d externalId=%s", node["name"], parent_id, node["dn"])
                    else:
                        created = self.ydx.create_department(
                            name=node["name"] or node["dn"].split(",")[0],
                            parent_id=parent_id,
                            external_id=node["dn"],
                            description=node.get("description", ""),
                        )
                        new_id = int(created["id"])
                        self.dept_by_dn[dn_key] = new_id
                        self.dept_by_id[new_id] = created
                        self.report.created_departments += 1
                        log.info("Создано подразделение %r -> id=%d", node["name"], new_id)
                else:
                    dept = self.dept_by_id.get(existing_id, {})
                    patch: dict[str, Any] = {}
                    desired_name = node["name"] or ""
                    if dept.get("name") != desired_name:  # переименование в ALD Pro
                        patch["name"] = desired_name
                    if int(dept.get("parentId", dept.get("parent_id", -1))) != parent_id:  # перемещение
                        patch["parentId"] = parent_id
                    if node.get("description") and dept.get("description") != node["description"]:
                        patch["description"] = node["description"]
                    if patch:
                        if dry:
                            log.info("[dry-run] UPDATE dept id=%d patch=%s", existing_id, patch)
                        else:
                            self.ydx.update_department(existing_id, patch)
                            dept.update(patch)
                            self.report.updated_departments += 1
                            log.info("Обновлено подразделение id=%d: %s", existing_id, patch)
            except (Yandex360Error, AldProError) as exc:
                self._error(f"Синхронизация подразделения {node['dn']}", exc)

        # удаления: было в прошлом снимке, нет в текущем поддереве
        removed_dns = set(self.state.ou_snapshot) - current
        # удаляем снизу вверх (сначала более глубокие DN)
        for dn_key in sorted(removed_dns, key=lambda k: k.count(","), reverse=True):
            dept_id = self.dept_by_dn.get(dn_key)
            if dept_id is None:
                continue
            if not self.cfg.sync.delete_departments:
                log.warning("Подразделение id=%d (%s) отсутствует в ALD Pro — удаление запрещено конфигом", dept_id, dn_key)
                continue
            try:
                if dry:
                    log.info("[dry-run] DELETE dept id=%d", dept_id)
                else:
                    self.ydx.delete_department(dept_id)
                    self.report.deleted_departments += 1
                    log.info("Удалено подразделение id=%d", dept_id)
                    self.dept_by_dn.pop(dn_key, None)
                    self.dept_by_id.pop(dept_id, None)
            except Yandex360Error as exc:
                # по документации удаление недоступно для непустого подразделения
                self._error(f"Удаление подразделения id={dept_id}", exc)

    # -------------------------------------------------------- step: sync users
    def index_yandex_users(self) -> None:
        """UserService_List -> индексы externalId->userId и nickname->userId."""
        for user in self.ydx.list_users():
            uid = str(user["id"])
            ext = user.get("externalId") or user.get("external_id")
            if ext:
                self.user_by_extid[str(ext)] = uid
            nick = user.get("nickname")
            if nick:
                self.user_by_nick[str(nick).lower()] = uid
        log.info("Яндекс 360: проиндексировано %d сотрудников", len(self.user_by_extid) + len(self.user_by_nick))

    def _resolve_dept_id_for_user(self, ou_dn: str) -> int | None:
        key = normalize_dn(ou_dn or "")
        if key == normalize_dn(self.cfg.sync.base_dn) or not key:
            return self.cfg.sync.root_department_id
        return self.dept_by_dn.get(key)

    def sync_users(self, ald_users: dict[str, dict[str, Any]]) -> None:
        dry = self.cfg.sync.dry_run
        initial_password = os.environ.get(self.cfg.yandex360.initial_password_env, "")

        for login, entry in sorted(ald_users.items()):
            list_item = entry["list_item"]
            try:
                full = self.ald.get_user(login)
                proxy = self.ald.get_proxy_addresses(login)
            except AldProError as exc:
                self._error(f"Чтение пользователя {login}", exc)
                continue
            entry["full"] = full
            entry["proxy"] = proxy

            ou_dn = full.get("user_organizational_unit_dn") or list_item.get("userlistitem_organizational_unit_dn") or ""
            dept_id = self._resolve_dept_id_for_user(ou_dn)
            if dept_id is None:
                self._error(f"Пользователь {login}", RuntimeError(f"подразделение {ou_dn!r} не синхронизировано"))
                continue

            nickname = to_nickname(login, self.cfg.sync.login_map_translit)
            email = pick_email(full, proxy, self.mail_domain, login)
            contacts = build_contacts(full, email)
            desired_enabled = not bool(full.get("user_locked", list_item.get("userlistitem_locked", False)))

            common = {
                "departmentId": dept_id,
                "name": {
                    "first": full.get("user_first_name") or "",
                    "last": full.get("user_last_name") or "",
                    "middle": full.get("user_middle_name") or "",
                },
                "position": full.get("user_title") or "",
                "contacts": contacts,
                "displayName": full.get("user_common_name") or "",
            }

            user_id = self.user_by_extid.get(login) or self.user_by_nick.get(nickname)
            try:
                if user_id is None:
                    body = {**common, "nickname": nickname, "externalId": login}
                    if initial_password:
                        body["password"] = initial_password
                        body["passwordChangeRequired"] = self.cfg.yandex360.password_change_required
                    if dry:
                        log.info("[dry-run] CREATE user login=%s nickname=%s dept=%d", login, nickname, dept_id)
                    else:
                        created = self.ydx.create_user(body)
                        self.user_by_extid[login] = str(created["id"])
                        self.user_by_nick[nickname] = str(created["id"])
                        self.report.created_users += 1
                        log.info("Создан сотрудник %s -> id=%s", login, created.get("id"))
                else:
                    patch = dict(common)
                    if not desired_enabled:
                        patch["isEnabled"] = False
                    if dry:
                        log.info("[dry-run] UPDATE user login=%s id=%s fields=%s", login, user_id, sorted(patch))
                    else:
                        self.ydx.update_user(user_id, patch)
                        self.report.updated_users += 1
                        log.info("Обновлён сотрудник %s (id=%s): отдел=%s, ФИО обновлены", login, user_id, dept_id)
            except Yandex360Error as exc:
                self._error(f"Синхронизация пользователя {login}", exc)

    # ------------------------------------------- step: removals & lock states
    def process_removed_users(self, ald_users: dict[str, dict[str, Any]]) -> None:
        """Обрабатывает удалённых (корзина ALD Pro, метод 6.1) и пропавших из поддерева пользователей.

        В API Яндекс 360 НЕТ метода удаления сотрудника (подтверждено по документации),
        поэтому выполняется блокировка ``isEnabled=false`` и/или увольнение ``isDismissed=true``
        методом UserService_Update.
        """
        if self.cfg.sync.on_removed_user == "none":
            return
        dry = self.cfg.sync.dry_run

        preserved_logins = {p.get("userlistitem_login") for p in self.ald.iter_preserved_users()}
        vanished = set(self.state.user_snapshot) - set(ald_users) - preserved_logins
        removed = (preserved_logins | vanished) - set(ald_users)

        for login in sorted(x for x in removed if x):
            user_id = self.user_by_extid.get(login) or self.user_by_nick.get(
                to_nickname(login, self.cfg.sync.login_map_translit)
            )
            if not user_id:
                continue
            patch: dict[str, Any] = {"isEnabled": False}
            if self.cfg.sync.on_removed_user == "dismiss":
                patch["isDismissed"] = True
            try:
                if dry:
                    log.info("[dry-run] REMOVE->UPDATE user login=%s id=%s patch=%s", login, user_id, patch)
                else:
                    self.ydx.update_user(user_id, patch)
                    if self.cfg.sync.on_removed_user == "dismiss":
                        self.report.dismissed_users += 1
                    else:
                        self.report.blocked_users += 1
                    log.info("Сотрудник %s удалён в ALD Pro -> в Яндекс 360 применён патч %s", login, patch)
            except Yandex360Error as exc:
                self._error(f"Обработка удаления пользователя {login}", exc)

    # ------------------------------------------------------------ main entry
    def run(self) -> SyncReport:
        started_at = utcnow_iso()
        log.info(
            "Старт синхронизации: режим=%s%s, baseDN=%s",
            ("полная (первичная)" if (self.cfg.sync.mode == "full" or self.state.is_first_run) else "инкрементальная"),
            ", DRY-RUN" if self.cfg.sync.dry_run else "",
            self.cfg.sync.base_dn,
        )

        departments = self.read_ald_departments()
        self.index_yandex_departments()
        self.sync_departments(departments)

        self.index_yandex_users()
        ald_users = self.read_ald_users(departments)
        self.sync_users(ald_users)
        self.process_removed_users(ald_users)

        # обновление снимка состояния
        if not self.cfg.sync.dry_run:
            self.state.ou_snapshot = {
                normalize_dn(n["dn"]): {"name": n["name"] or "", "parent_dn": n["parent_dn"] or ""}
                for n in departments
            }
            self.state.user_snapshot = {
                login: {
                    "ou_dn": normalize_dn((e.get("full") or e["list_item"]).get(
                        "user_organizational_unit_dn"
                    ) or e["list_item"].get("userlistitem_organizational_unit_dn") or ""),
                    "locked": bool((e.get("full") or {}).get("user_locked", e["list_item"].get("userlistitem_locked"))),
                }
                for login, e in ald_users.items()
            }
            self.state.last_full_sync_at = started_at
            self.state.save()

        log.info("Завершение синхронизации: %s", self.report.as_dict())
        return self.report
