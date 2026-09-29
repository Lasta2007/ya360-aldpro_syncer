"""Настройки модуля синхронизации ALD Pro -> Яндекс 360.

Все настройки выносятся в YAML/JSON-файл и/или переменные окружения.
Приоритет: переменные окружения (префикс ``A2Y_``) > файл конфигурации > значения по умолчанию.

Пример файла конфигурации см. в ``config/config.example.yaml``.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal, Optional

import yaml
from pydantic import BaseModel, Field, field_validator


class AldProSettings(BaseModel):
    """Подключение к ALD Pro (раздел 1.3.1 «Аутентификация» документации API ALD Pro 3.2.0)."""

    base_url: str = Field(..., description="Базовый URL ALD Pro, напр. https://aldpro.example.ru/ad")
    login: str = Field(..., description="Логин сервисной учётной записи (POST /api/ds/login)")
    password: str = Field(..., description="Пароль сервисной учётной записи")
    verify_ssl: bool | str = True
    timeout: float = 30.0
    page_size: int = Field(500, ge=1, description="Значение QUERY-параметра limit для списочных методов")


class Yandex360Settings(BaseModel):
    """Подключение к Яндекс 360 API (раздел «Доступ к API», doc/ru/access)."""

    oauth_token: str = Field(..., description="OAuth-токен, заголовок Authorization: OAuth <token>")
    org_id: int = Field(..., description="Идентификатор организации (orgId)")
    api_host: str = Field("cloud-api.yandex.net", description="cloud-api.yandex.net (актуальный) или api360.yandex.net")
    use_ref_paths: bool = Field(
        True,
        description="True -> пути /directory/v1/org/{orgId}/... (раздел ref/*), "
        "False -> пути /v1/directory/organizations/{org_id}/... (раздел directory/*)",
    )
    timeout: float = 30.0
    per_page: int = Field(1000, ge=1, le=1000, description="QUERY-параметр _perPage метода DepartmentService_List")
    # Пароль, задаваемый создаваемым сотрудникам (обязательное поле UserService_Create).
    initial_password_env: str = "A2Y_YANDEX360_INITIAL_PASSWORD"
    password_change_required: bool = True


class SyncSettings(BaseModel):
    base_dn: str = Field(..., description="DN подразделения-корня в ALD Pro, от которого идёт обход дерева")
    root_department_id: int = Field(
        ..., description="id корневого подразделения в Яндекс 360 (родитель для подразделений из ALD Pro)"
    )
    state_path: str = Field("state/sync_state.json", description="Файл состояния для инкрементальной синхронизации")
    mode: Literal["full", "incremental"] = "incremental"
    dry_run: bool = False
    delete_departments: bool = Field(False, description="Разрешить DepartmentService_Delete для удалённых OU")
    on_removed_user: Literal["block", "dismiss", "none"] = Field(
        "block",
        description="Действие в Яндекс 360 при удалении пользователя в ALD Pro (корзина): "
        "block -> isEnabled=false, dismiss -> isDismissed=true, none -> ничего",
    )
    schedule_cron: str = Field("0 3 * * *", description="Расписание запуска (cron, интерпретируется планировщиком ОС)")
    max_retries: int = 3
    retry_backoff: float = 1.5
    login_map_translit: bool = Field(True, description="Транслитерация кириллического логина для nickname")


class LoggingSettings(BaseModel):
    level: str = "INFO"
    file: Optional[str] = "logs/ald2ydx.log"
    format: str = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"


class Settings(BaseModel):
    ald_pro: AldProSettings
    yandex360: Yandex360Settings
    sync: SyncSettings
    logging: LoggingSettings = LoggingSettings()

    @field_validator("logging")
    @classmethod
    def _check_logging(cls, v: LoggingSettings) -> LoggingSettings:
        return v


_ENV_PREFIX = "A2Y_"


def _env_overrides() -> dict[str, Any]:
    """Переменные вида A2Y_ALD_PRO_BASE_URL -> {'ald_pro': {'base_url': ...}}."""
    mapping = {
        "A2Y_ALD_PRO_BASE_URL": ("ald_pro", "base_url"),
        "A2Y_ALD_PRO_LOGIN": ("ald_pro", "login"),
        "A2Y_ALD_PRO_PASSWORD": ("ald_pro", "password"),
        "A2Y_YANDEX360_OAUTH_TOKEN": ("yandex360", "oauth_token"),
        "A2Y_YANDEX360_ORG_ID": ("yandex360", "org_id"),
        "A2Y_YANDEX360_API_HOST": ("yandex360", "api_host"),
        "A2Y_SYNC_BASE_DN": ("sync", "base_dn"),
        "A2Y_SYNC_ROOT_DEPARTMENT_ID": ("sync", "root_department_id"),
        "A2Y_SYNC_MODE": ("sync", "mode"),
        "A2Y_SYNC_STATE_PATH": ("sync", "state_path"),
        "A2Y_LOG_LEVEL": ("logging", "level"),
    }
    result: dict[str, Any] = {}
    for env_name, (section, key) in mapping.items():
        value = os.environ.get(env_name)
        if value is None:
            continue
        if key in ("org_id", "root_department_id"):
            typed: Any = int(value)
        elif section == "sync" and key == "mode":
            typed = value
        else:
            typed = value
        result.setdefault(section, {})[key] = typed
    return result


def load_settings(path: str | os.PathLike[str] | None = None) -> Settings:
    """Загружает конфигурацию из файла (YAML/JSON) с переопределением env-переменными."""
    data: dict[str, Any] = {}
    candidates: list[str] = []
    if path:
        candidates.append(str(path))
    candidates += [os.environ.get("A2Y_CONFIG", ""), "config/config.yaml", "config/config.yml", "config/config.json"]
    for cand in candidates:
        if cand and Path(cand).is_file():
            raw = Path(cand).read_text(encoding="utf-8")
            data = json.loads(raw) if cand.endswith(".json") else yaml.safe_load(raw)
            data = data or {}
            break

    overrides = _env_overrides()
    for section, values in overrides.items():
        data.setdefault(section, {}).update(values)

    return Settings.model_validate(data)
