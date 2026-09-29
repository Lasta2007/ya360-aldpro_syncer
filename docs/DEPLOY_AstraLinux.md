# Развёртывание ald2ydx на Astra Linux (Смоленск/Воронеж, 1.7–1.8)

## 0. Требования
- Python **3.9+** (код использует `from __future__ import annotations`, проверено на 3.11).
  В Astra 1.7.x в репозитории «Обновления» есть `python3` 3.9/3.11; в 1.8 — 3.11+.
- Сетевой доступ сервера к ALD Pro (`https://ald...:443`) и к `cloud-api.yandex.net`/`api360.yandex.net` (443).
- Если используется мандатный контроль целостности (ПАРТОЛ/МКИ) — размещайте код в зоне,
  где запись разрешена сервисному пользователю, либо работайте без МКИ на этом узле.

## 1. Установка системных пакетов
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ca-certificates
# если нужен доступ из-под Fly/PARSEC-ограничений — убедитесь, что права выданы штатными средствами (fly-*),
# обычный chmod/chown также работают.
```

## 2. Развёртывание кода
```bash
sudo useradd -r -m -d /var/lib/ald2ydx -s /usr/sbin/nologin ald2ydx
sudo mkdir -p /opt/ald2ydx /etc/ald2ydx /var/log/ald2ydx
sudo cp -r ald2ydx requirements.txt /opt/ald2ydx/          # из этого репозитория
sudo chown -R root:ald2ydx /opt/ald2ydx && sudo chmod -R g-w,o-rwx /opt/ald2ydx

sudo -u ald2ydx python3 -m venv /opt/ald2ydx/venv
sudo /opt/ald2ydx/venv/bin/pip install --no-cache-dir -r /opt/ald2ydx/requirements.txt
# Для air-gapped: скачайте колёса на машине с интернетом (pip download -r requirements.txt -d wheels/)
# и поставьте: pip install --no-index --find-links wheels/ -r requirements.txt
```

## 3. Конфигурация
```bash
sudo cp ald2ydx/config/config.example.yaml /etc/ald2ydx/config.yaml
sudoedit /etc/ald2ydx/config.yaml        # base_url, org_id, base_dn, root_department_id, state_path
sudo cp deploy/secret.env.example /etc/ald2ydx/secret.env
sudo chmod 600 /etc/ald2ydx/secret.env
sudo chown root:ald2ydx /etc/ald2ydx/secret.env
sudo mkdir -p /var/lib/ald2ydx && sudo chown ald2ydx:ald2ydx /var/lib/ald2ydx
sudo touch /var/log/ald2ydx/sync.log && sudo chown ald2ydx:ald2ydx /var/log/ald2ydx
```
Секреты задаются переменными окружения (переопределяют YAML):
`A2Y_ALD_PRO_PASSWORD`, `A2Y_YANDEX360_OAUTH_TOKEN`, `A2Y_YANDEX360_INITIAL_PASSWORD`.

## 4. Проверка вручную (dry-run, ничего не меняет в Яндекс 360)
```bash
sudo -u ald2ydx env A2Y_CONFIG=/etc/ald2ydx/config.yaml \
    /opt/ald2ydx/venv/bin/python -m ald2ydx --dry-run --mode full
echo $?   # 0 — успех, 1 — есть ошибки синхронизации, 2 — ошибка конфигурации
```
При внутреннем самоподписанном сертификате ALD Pro укажите в конфиге
`ald_pro.verify_ssl: /etc/ssl/certs/aldpro-ca.pem`.

## 5. Запуск по расписанию (systemd timer)
```bash
sudo cp deploy/systemd/ald2ydx.service deploy/systemd/ald2ydx.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ald2ydx.timer
systemctl list-timers | grep ald2ydx
```
Однократный запуск: `sudo systemctl start ald2ydx.service`
Логи: `journalctl -u ald2ydx.service -f` и `/var/log/ald2ydx/sync.log`.

## 6. Настройка расписания
Интервал задаётся в `ald2ydx.timer` параметром `OnUnitActiveSec=` (по умолчанию 1h).
Для cron вместо timer:
```cron
# crontab -e для пользователя ald2ydx
0 * * * * /opt/ald2ydx/venv/bin/python -m ald2ydx >> /var/log/ald2ydx/cron.log 2>&1
```
(при cron добавьте Environment через скрипт-обёртку или строку `A2Y_CONFIG=... python -m ald2ydx`).

## 7. Обновление версии
```bash
sudo rsync -a --delete ald2ydx/ /opt/ald2ydx/ald2ydx/   # только пакет кода, venv и конфиги не трогаем
sudo /opt/ald2ydx/venv/bin/pip install -r /opt/ald2ydx/requirements.txt
sudo systemctl restart ald2ydx.timer
```

## 8. Диагностика типовых проблем
| Симптом | Причина/решение |
|---|---|
| `Ошибка загрузки конфигурации` (rc=2) | Не задан обязательный параметр (org_id, base_dn и т.п.) — см. сообщения pydantic |
| 401 от ALD Pro (`POST /api/ds/login`) | Неверные учётные данные сервисной УЗ; проверьте блокировку УЗ в самом ALD |
| 403 `OAuth token ...` от Яндекс 360 | Токен просрочен/не имеет нужных прав организации; перевыпустите токен |
| SSL errors | Добавьте CA в доверенные (`update-ca-certificates`) или `verify_ssl: <путь к pem>` |
| Пустой отчёт при incremental | Проверьте `sync.state_path`: файл состояния доступен на запись пользователю `ald2ydx` |
