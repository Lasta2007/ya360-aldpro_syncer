"""Централизованная настройка логирования модуля."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from .settings import LoggingSettings


def setup_logging(cfg: LoggingSettings) -> logging.Logger:
    root = logging.getLogger("ald2ydx")
    root.setLevel(cfg.level.upper())
    root.handlers.clear()

    formatter = logging.Formatter(cfg.format)

    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    root.addHandler(stream)

    if cfg.file:
        Path(cfg.file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(cfg.file, encoding="utf-8")
        fh.setFormatter(formatter)
        root.addHandler(fh)

    root.propagate = False
    return root


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"ald2ydx.{name}")
