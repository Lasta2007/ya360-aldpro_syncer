"""Сопоставление (mapping) сущностей ALD Pro <-> Яндекс 360 и состояние инкрементальной синхронизации.

Стратегия сопоставления:
- Подразделение: ключом является DN подразделения ALD Pro. Он сохраняется в поле
  ``externalId`` подразделения Яндекс 360 (DepartmentService_Create/Update поддерживают
  ``externalId`` — «произвольный внешний идентификатор подразделения»). Повторная синхронизация
  строит индекс externalId -> departmentId.
- Сотрудник: ключом является логин ALD Pro (userlistitem_login / user_login). Он сохраняется
  в поле ``externalId`` сотрудника Яндекс 360 (UserService_Create/Update поддерживают
  ``externalId`` — «произвольный внешний идентификатор сотрудника»). Повторная синхронизация
  строит индекс externalId -> id пользователя; additionally используется индекс по nickname.

Файл состояния хранит контрольную точку последнего полного прохода (UTC ISO8601) и снимок
дерева ALD Pro (dn -> {name,parent_dn}), чтобы детектировать переименования, перемещения
и удаления без специализированных API (их нет ни в ALD Pro API 3.2.0, ни в Яндекс 360 API).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class SyncState:
    path: Path
    last_full_sync_at: Optional[str] = None
    #: dn подразделения -> {"name":..., "parent_dn":...}
    ou_snapshot: dict[str, dict[str, str]] = field(default_factory=dict)
    #: login пользователя -> {"ou_dn":..., "common_name":..., "locked": bool, "removed_at": str|None}
    user_snapshot: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "SyncState":
        p = Path(path)
        if not p.is_file():
            return cls(path=p)
        raw = json.loads(p.read_text(encoding="utf-8"))
        return cls(
            path=p,
            last_full_sync_at=raw.get("last_full_sync_at"),
            ou_snapshot=raw.get("ou_snapshot", {}),
            user_snapshot=raw.get("user_snapshot", {}),
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "last_full_sync_at": self.last_full_sync_at,
            "ou_snapshot": self.ou_snapshot,
            "user_snapshot": self.user_snapshot,
        }
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    @property
    def is_first_run(self) -> bool:
        return self.last_full_sync_at is None


# --------------------------------------------------------------------------- helpers
def normalize_dn(dn: str) -> str:
    """Нормализация DN для сравнения: нижний регистр, схлопывание пробелов после ','.

    LDAP DN нечувствителен к регистру атрибутов/значений; нормализация нужна,
    чтобы перемещение пользователя между OU с одинаковым именем не давало ложных diffs.
    """
    parts = [p.strip().lower() for p in dn.split(",")]
    return ",".join(parts)


_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def to_nickname(login: str, translit: bool = True) -> str:
    """Логин ALD Pro -> nickname Яндекс 360.

    nickname используется как логин сотрудника (UserService_Create: «Логин сотрудника»).
    Кириллические логины транслитерируются и приводятся к нижнему регистру;
    исходный логин всегда сохраняется в externalId, поэтому транслитерация безопасна.
    """
    value = login.strip().lower()
    if not translit:
        return value
    out: list[str] = []
    for ch in value:
        if ch in _TRANSLIT:
            out.append(_TRANSLIT[ch])
        elif ch.isascii() and (ch.isalnum() or ch in "._-"):
            out.append(ch)
        else:
            out.append("_")
    return "".join(out) or value


def pick_email(user: dict[str, Any], proxy_addresses: list[dict[str, str]], domain: str, login: str) -> str:
    """Определяет основной e-mail сотрудника Яндекс 360.

    Приоритет: SMTP (основной, заглавный) из proxyAddresses (ALD Pro, раздел 8.19) ->
    user_mail (ALD Pro, раздел 8.4) -> <nickname>@<domain> (домен берётся из конфига org-домена,
    т.к. API Яндекс 360 позволяет задавать email только через алиасы/контакты).
    """
    main = next((p["body"] for p in proxy_addresses if p.get("type") == "SMTP"), None)
    if main:
        return main
    alt = next((p["body"] for p in proxy_addresses if p.get("type") == "smtp"), None)
    if alt:
        return alt
    mail = user.get("user_mail")
    if mail:
        return mail
    return f"{to_nickname(login)}@{domain}" if domain else ""


def build_contacts(user: dict[str, Any], email: str) -> list[dict[str, str]]:
    """Формирует contacts для UserService_Create/Update.

    Допустимые type (по документации): email, phone_extension, phone, site, icq, twitter, skype.
    Маппинг ALD Pro (раздел 8.4): user_mobile -> phone, user_telephone_number -> phone,
    user_telephone_number_ext -> phone_extension, e-mail -> email.
    """
    contacts: list[dict[str, str]] = []
    if email:
        contacts.append({"type": "email", "value": email})
    for number in _as_list(user.get("user_mobile")):
        contacts.append({"type": "phone", "value": number, "label": "mobile"})
    for number in _as_list(user.get("user_telephone_number")):
        contacts.append({"type": "phone", "value": number, "label": "work"})
    ext = user.get("user_telephone_number_ext")
    if ext:
        contacts.append({"type": "phone_extension", "value": str(ext)})
    return contacts


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    return [str(value)]


def user_fingerprint(user: dict[str, Any]) -> dict[str, Any]:
    """Контрольные поля пользователя для детекции изменений при инкрементальном проходе."""
    return {
        "last": user.get("user_last_name") or "",
        "first": user.get("user_first_name") or "",
        "middle": user.get("user_middle_name") or "",
        "title": user.get("user_title") or "",
        "ou_dn": normalize_dn(user.get("user_organizational_unit_dn") or ""),
        "locked": bool(user.get("user_locked")),
        "mail": user.get("user_mail") or "",
    }
