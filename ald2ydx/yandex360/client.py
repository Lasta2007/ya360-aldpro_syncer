"""Клиент Яндекс 360 API (https://yandex.ru/dev/api360/doc/ru/).

Используются ТОЛЬКО методы из официальной документации:

- UserService_List    GET    /directory/v1/org/{orgId}/users                      (ref/UserService)
- UserService_Create  POST   /directory/v1/org/{orgId}/users                      (ref/UserService)
- UserService_Update  PATCH  /directory/v1/org/{orgId}/users/{userId}             (ref/UserService)
- DepartmentService_List   GET   /directory/v1/org/{orgId}/departments            (ref/DepartmentService)
- DepartmentService_Create POST  /directory/v1/org/{orgId}/departments            (ref/DepartmentService)
- DepartmentService_Update PATCH /directory/v1/org/{orgId}/departments/{id}       (ref/DepartmentService)
- DepartmentService_Delete DELETE /directory/v1/org/{orgId}/departments/{id}      (ref/DepartmentService)

Аутентификация — OAuth-токен в заголовке ``Authorization: OAuth <token>`` (раздел «Доступ к API»).

ВАЖНО (подтверждено по документации): в API Яндекс 360 ОТСУТСТВУЕТ метод удаления
сотрудника. Удаление сотрудника в источнике трактуется как блокировка
(``isEnabled=false``) и/или пометка об увольнении (``isDismissed=true``) через UserService_Update.
"""

from __future__ import annotations

import time
from typing import Any, Optional

import httpx

from ..logging_setup import get_logger
from ..settings import Yandex360Settings

log = get_logger("ydx")


class Yandex360Error(RuntimeError):
    def __init__(self, status: int, message: str, body: Any = None) -> None:
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.message = message
        self.body = body


class Yandex360Client:
    def __init__(self, settings: Yandex360Settings, max_retries: int = 3, retry_backoff: float = 1.5) -> None:
        self._s = settings
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._http = httpx.Client(
            base_url=f"https://{settings.api_host}",
            timeout=settings.timeout,
            headers={"Authorization": f"OAuth {settings.oauth_token}", "Content-Type": "application/json"},
        )

    # ------------------------------------------------------------- internals
    def _paths(self, resource: str, ident: Optional[str] = None) -> str:
        """Формирует путь в зависимости от выбранного варианта API (см. doc/ru/access.md)."""
        if self._s.use_ref_paths:
            base = f"/directory/v1/org/{self._s.org_id}/{resource}"
        else:
            base = f"/v1/directory/organizations/{self._s.org_id}/{resource}"
        return f"{base}/{ident}" if ident is not None else base

    def _request(self, method: str, path: str, *, json_body: Optional[dict[str, Any]] = None,
                 params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        last_exc: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                resp = self._http.request(method, path, json=json_body, params=params)
            except httpx.TransportError as exc:  # сеть/таймаут
                last_exc = exc
                log.warning("%s %s: транспортная ошибка (%s), попытка %d/%d",
                            method, path, exc.__class__.__name__, attempt, self._max_retries)
                time.sleep(self._retry_backoff**attempt)
                continue

            if resp.status_code in (429, 500, 502, 503, 504):
                body = self._safe_json(resp)
                msg = body.get("message", "") if isinstance(body, dict) else resp.text[:200]
                last_exc = Yandex360Error(resp.status_code, f"retryable: {msg}", body)
                log.warning("%s %s: HTTP %d (%s), попытка %d/%d", method, path, resp.status_code, msg,
                            attempt, self._max_retries)
                time.sleep(self._retry_backoff**attempt)
                continue

            if resp.status_code >= 400:
                body = self._safe_json(resp)
                msg = body.get("message", resp.text[:300]) if isinstance(body, dict) else resp.text[:300]
                raise Yandex360Error(resp.status_code, msg, body)

            if not resp.content:
                return {}
            return self._safe_json(resp)

        assert last_exc is not None
        raise last_exc

    @staticmethod
    def _safe_json(resp: httpx.Response) -> Any:
        try:
            return resp.json()
        except ValueError:
            return resp.text

    # ---------------------------------------------------------- departments
    def list_departments(self) -> list[dict[str, Any]]:
        """DepartmentService_List: GET /directory/v1/org/{orgId}/departments (_page/_perPage)."""
        result: list[dict[str, Any]] = []
        page = 1
        while True:
            payload = self._request(
                "GET",
                self._paths("departments"),
                params={"_page": page, "_perPage": self._s.per_page},
            )
            items = payload.get("data") or payload.get("departments") or payload.get("items") or []
            result.extend(items)
            pages = int(payload.get("pages") or payload.get("_pages") or 1)
            if page >= pages or not items:
                break
            page += 1
        return result

    def create_department(self, name: str, parent_id: int, external_id: str, description: str = "") -> dict[str, Any]:
        """DepartmentService_Create: POST /directory/v1/org/{orgId}/departments."""
        body: dict[str, Any] = {"name": name, "parentId": parent_id, "externalId": external_id}
        if description:
            body["description"] = description
        if self._s.use_ref_paths is False:
            body = {  # legacy-путь использует snake_case
                "name": name,
                "parent_id": parent_id,
                "external_id": external_id,
            }
            if description:
                body["description"] = description
        return self._request("POST", self._paths("departments"), json_body=body)

    def update_department(self, department_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        """DepartmentService_Update: PATCH /directory/v1/org/{orgId}/departments/{departmentId}.

        Изменяются значения только тех параметров, которые переданы в запросе.
        """
        return self._request("PATCH", self._paths("departments", str(department_id)), json_body=fields)

    def delete_department(self, department_id: int) -> dict[str, Any]:
        """DepartmentService_Delete: DELETE /directory/v1/org/{orgId}/departments/{departmentId}."""
        return self._request("DELETE", self._paths("departments", str(department_id)))

    # ---------------------------------------------------------------- users
    def list_users(self) -> list[dict[str, Any]]:
        """UserService_List: GET /directory/v1/org/{orgId}/users (_page/_perPage, max _perPage=1000)."""
        result: list[dict[str, Any]] = []
        page = 1
        while True:
            payload = self._request("GET", self._paths("users"), params={"_page": page, "_perPage": self._s.per_page})
            items = payload.get("users") or payload.get("data") or payload.get("items") or []
            result.extend(items)
            pages = int(payload.get("pages") or 1)
            if page >= pages or not items:
                break
            page += 1
        return result

    def create_user(self, body: dict[str, Any]) -> dict[str, Any]:
        """UserService_Create: POST /directory/v1/org/{orgId}/users."""
        return self._request("POST", self._paths("users"), json_body=body)

    def update_user(self, user_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        """UserService_Update: PATCH /directory/v1/org/{orgId}/users/{userId}."""
        return self._request("PATCH", self._paths("users", user_id), json_body=fields)

    def close(self) -> None:
        try:
            self._http.close()
        except Exception:  # pragma: no cover
            pass

    def __enter__(self) -> "Yandex360Client":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
