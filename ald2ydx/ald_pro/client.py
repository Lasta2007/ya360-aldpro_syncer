"""Клиент API ALD Pro 3.2.0.

Используются ТОЛЬКО методы из «Документация API ALD Pro для 3.2.0»:

- 2.1  POST /api/ds/login                                        — аутентификация (раздел 1.3.1/2.1)
- 7.9  GET  /api/ds/organizational-units/{ouDN}/organizational-units — дочерние подразделения
- 7.6  GET  /api/ds/organizational-units/{ouDN}                  — параметры подразделения
- 7.21 GET  /api/ds/organizational-units/{ouDN}/users-list       — пользователи подразделения
- 8.4  GET  /api/ds/users/{userName}                             — параметры пользователя
- 8.19 GET  /api/ds/users/{userName}/proxy_addresses             — proxyAddresses пользователя
- 6.1  GET  /api/ds/preserved/users                              — список пользователей в корзине
"""

from __future__ import annotations

import urllib.parse
from typing import Any, Iterator, Optional

import httpx

from ..logging_setup import get_logger
from ..settings import AldProSettings

log = get_logger("ald")


class AldProError(RuntimeError):
    """Ошибка API ALD Pro. По документации сервер возвращает стандартное сообщение об ошибке с кодом 500."""


def _quote_dn(dn: str) -> str:
    """DN подставляется в PATH-параметр, поэтому экранируется по правилам URL."""
    return urllib.parse.quote(dn, safe="")


class AldProClient:
    def __init__(self, settings: AldProSettings) -> None:
        self._s = settings
        self._http = httpx.Client(
            base_url=settings.base_url.rstrip("/"),
            timeout=settings.timeout,
            verify=settings.verify_ssl,
            headers={"accept": "application/json, text/plain, */*"},
            follow_redirects=False,
        )
        self._authenticated = False

    # ------------------------------------------------------------------ auth
    def login(self) -> None:
        """2.1 Аутентифицироваться на портале: POST /api/ds/login.

        Ответ содержит ``{"success": true}``; сессия передаётся cookie из заголовка
        ``Set-cookie`` (httpx хранит их автоматически в cookies клиента). Срок сессии — 23 часа.
        """
        resp = self._http.post(
            "/api/ds/login",
            json={"data": {"login": self._s.login, "password": self._s.password}},
            headers={"Content-Type": "application/json"},
        )
        payload = self._parse(resp, "POST /api/ds/login")
        if not payload.get("success"):
            raise AldProError(f"ALD Pro login failed: {payload}")
        self._authenticated = True
        log.info("ALD Pro: успешная аутентификация (POST /api/ds/login)")

    def close(self) -> None:
        try:
            self._http.close()
        except Exception:  # pragma: no cover
            pass

    def __enter__(self) -> "AldProClient":
        self.login()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ------------------------------------------------------------- internals
    def _parse(self, resp: httpx.Response, method_desc: str) -> dict[str, Any]:
        if resp.status_code >= 400:
            raise AldProError(f"{method_desc}: HTTP {resp.status_code}: {resp.text[:500]}")
        try:
            data = resp.json()
        except ValueError as exc:
            raise AldProError(f"{method_desc}: ответ не является JSON: {resp.text[:200]}") from exc
        if isinstance(data, dict) and data.get("success") is False:
            raise AldProError(f"{method_desc}: success=false: {data}")
        return data if isinstance(data, dict) else {"data": data}

    def _get(self, path: str, params: Optional[dict[str, Any]] = None, desc: str = "") -> dict[str, Any]:
        if not self._authenticated:
            self.login()
        resp = self._http.get(path, params=params)
        # Сессия живёт 23 часа; при протухании — повторный логин и один retry.
        if resp.status_code in (401, 403):
            log.warning("%s: ответ %s, перелогиниваюсь", desc or path, resp.status_code)
            self.login()
            resp = self._http.get(path, params=params)
        return self._parse(resp, desc or f"GET {path}")

    # ----------------------------------------------------------- departments
    def iter_children(self, parent_dn: str) -> Iterator[dict[str, Any]]:
        """7.9 Получить список дочерних организаций подразделения (пагинация limit/offset)."""
        offset = 0
        path_tmpl = "/api/ds/organizational-units/{}/organizational-units"
        while True:
            payload = self._get(
                path_tmpl.format(_quote_dn(parent_dn)),
                params={"limit": self._s.page_size, "offset": offset},
                desc=f"GET 7.9 children of {parent_dn}",
            )
            items = payload.get("data") or []
            for item in items:
                yield item
            total = int(payload.get("total") or 0)
            offset += len(items)
            if not items or offset >= total:
                break

    def get_ou_params(self, ou_dn: str) -> dict[str, Any]:
        """7.6 Получить параметры подразделения (описание, руководитель, адрес)."""
        payload = self._get(
            f"/api/ds/organizational-units/{_quote_dn(ou_dn)}",
            desc=f"GET 7.6 ou {ou_dn}",
        )
        return payload.get("data") or {}

    def walk_subtree(self, base_dn: str) -> Iterator[dict[str, Any]]:
        """Обход дерева подразделений начиная с baseDN (BFS по методу 7.9).

        Элементы baseDN в выдачу НЕ включается — только его потомки.
        Возвращаются плоские словари: dn, name, parent_dn, is_leaf.
        """
        queue: list[str] = [base_dn]
        seen: set[str] = set()
        while queue:
            parent = queue.pop(0)
            for child in self.iter_children(parent):
                dn = child.get("organizationunitlistitem_dn")
                if not dn or dn in seen:
                    continue
                seen.add(dn)
                yield {
                    "dn": dn,
                    "name": child.get("organizationunitlistitem_display_name"),
                    "parent_dn": child.get("organizationunitlistitem_parent_dn") or parent,
                    "is_leaf": bool(child.get("organizationunitlistitem_is_leaf")),
                }
                queue.append(dn)

    # --------------------------------------------------------------- users
    def iter_users_of_ou(self, ou_dn: str) -> Iterator[dict[str, Any]]:
        """7.21 Получить список пользователей подразделения (limit/offset)."""
        offset = 0
        path = f"/api/ds/organizational-units/{_quote_dn(ou_dn)}/users-list"
        while True:
            payload = self._get(
                path,
                params={"limit": self._s.page_size, "offset": offset},
                desc=f"GET 7.21 users of {ou_dn}",
            )
            items = payload.get("data") or []
            for item in items:
                yield item
            total = int(payload.get("total") or 0)
            offset += len(items)
            if not items or offset >= total:
                break

    def get_user(self, user_name: str) -> dict[str, Any]:
        """8.4 Получить параметры пользователя."""
        payload = self._get(f"/api/ds/users/{_quote_dn(user_name)}", desc=f"GET 8.4 user {user_name}")
        data = payload.get("data")
        if isinstance(data, list):  # в описании ответа указан тип List[]
            data = data[0] if data else {}
        return data or {}

    def get_proxy_addresses(self, user_name: str) -> list[dict[str, str]]:
        """8.19 Получить перечень значений proxyAddresses пользователя."""
        payload = self._get(
            f"/api/ds/users/{_quote_dn(user_name)}/proxy_addresses",
            desc=f"GET 8.19 proxy_addresses {user_name}",
        )
        return [
            {"type": x.get("userproxyaddress_type", ""), "body": x.get("userproxyaddress_body", "")}
            for x in (payload.get("data") or [])
        ]

    def iter_preserved_users(self) -> Iterator[dict[str, Any]]:
        """6.1 Получить список пользователей в корзине (удаляемых источнике)."""
        offset = 0
        while True:
            payload = self._get(
                "/api/ds/preserved/users",
                params={"limit": self._s.page_size, "offset": offset},
                desc="GET 6.1 preserved users",
            )
            items = payload.get("data") or []
            for item in items:
                yield item
            total = int(payload.get("total") or 0)
            offset += len(items)
            if not items or offset >= total:
                break
