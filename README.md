# ya360-aldpro_syncer (ald2ydx)

Модуль синхронизации структуры подразделений и сотрудников из **ALD Pro 3.2.0** в **Яндекс 360**
(только методы, описанные в официальной документации: https://yandex.ru/dev/api360/doc/ru/ и
«Документация API ALD Pro для 3.2.0»).

## Быстрый старт (локально)
```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
cp ald2ydx/config/config.example.yaml config/config.yaml   # отредактировать
export A2Y_ALD_PRO_PASSWORD=... A2Y_YANDEX360_OAUTH_TOKEN=... A2Y_YANDEX360_INITIAL_PASSWORD=...
python -m ald2ydx --dry-run --mode full     # безопасная проверка
python -m ald2ydx                            # рабочая синхронизация
```
Коды возврата: 0 — успех, 1 — ошибки при синхронизации, 2 — ошибка конфигурации.

## Запуск на сервере с Astra Linux
Полная инструкция: [docs/DEPLOY_AstraLinux.md](docs/DEPLOY_AstraLinux.md).
Кратко:
```bash
# код -> /opt/ya360-aldpro_syncer, конфиг -> /etc/ald2ydx/config.yaml, секреты -> /etc/ald2ydx/secret.env (chmod 600)
cd /opt/ya360-aldpro_syncer && sudo -u ald2ydx ./venv/bin/python -m ald2ydx --dry-run --mode full
sudo cp deploy/systemd/ald2ydx.service deploy/systemd/ald2ydx.timer /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now ald2ydx.timer
systemctl status ald2ydx.service && journalctl -u ald2ydx.service -f
```

## Структура
- `ald2ydx/settings.py` — конфигурация (YAML + env `A2Y_*`, pydantic-валидация)
- `ald2ydx/__main__.py` — CLI: `python -m ald2ydx [--config] [--dry-run] [--mode]`
- `ald2ydx/ald_pro/client.py` — клиент ALD Pro (login 1.3.1, 7.9/7.6, 7.21, 8.4, 8.19, корзина 6.1)
- `ald2ydx/yandex360/client.py` — клиент Яндекс 360 (DepartmentService/UserService List/Create/Update/Delete)
- `ald2ydx/sync/engine.py`, `mapping.py` — конвейер snapshot-diff, сопоставление по externalId/DN/login
- `deploy/` — systemd unit/timer, пример secret.env
- `docs/` — инструкция по развёртыванию на Astra Linux
