"""Точка входа модуля синхронизации ALD Pro -> Яндекс 360.

Запуск:
    python -m ald2ydx --config /etc/ald2ydx/config.yaml [--dry-run] [--mode full|incremental]

Без аргументов конфигурация ищется в $A2Y_CONFIG, ./config/config.yaml.
Переменные окружения с префиксом A2Y_ переопределяют значения из файла.
"""

from __future__ import annotations

import argparse
import sys

from ald2ydx.ald_pro.client import AldProClient
from ald2ydx.logging_setup import setup_logging
from ald2ydx.settings import load_settings
from ald2ydx.sync.engine import DirectorySynchronizer
from ald2ydx.yandex360.client import Yandex360Client


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ald2ydx",
        description="Синхронизация подразделений и сотрудников из ALD Pro в Яндекс 360",
    )
    parser.add_argument("--config", "-c", help="Путь к YAML/JSON-файлу конфигурации")
    parser.add_argument("--dry-run", action="store_true", help="Не выполнять изменения в Яндекс 360")
    parser.add_argument("--mode", choices=["full", "incremental"], help="Режим синхронизации")
    args = parser.parse_args(argv)

    try:
        settings = load_settings(args.config)
    except Exception as exc:  # noqa: BLE001
        print(f"Ошибка загрузки конфигурации: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        settings.sync.dry_run = True
    if args.mode:
        settings.sync.mode = args.mode

    logger = setup_logging(settings.logging)
    logger.info(
        "Старт синхронизации: режим=%s, baseDN=%s, dry_run=%s",
        settings.sync.mode,
        settings.sync.base_dn,
        settings.sync.dry_run,
    )

    with AldProClient(settings.ald_pro) as ald, Yandex360Client(settings.yandex360) as ydx:
        engine = DirectorySynchronizer(settings=settings, ald=ald, ydx=ydx)
        try:
            report = engine.run()
        except Exception:  # noqa: BLE001
            logger.exception("Синхронизация завершилась с фатальной ошибкой")
            return 1

    logger.info("Отчёт: %s", report.as_dict())
    for err in report.errors:
        logger.error("Ошибка: %s", err)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
