# Развёртывание ya360-aldpro_syncer (ald2ydx) на Astra Linux (Смоленск/Воронеж, 1.7–1.8)

Код проекта размещается в **`/opt/ya360-aldpro_syncer`**. Конфигурация — в `/etc/ald2ydx/config.yaml`,
секреты — в `/etc/ald2ydx/secret.env`, состояние инкрементальной синхронизации — в `/var/lib/ald2ydx`,
логи — в `/var/log/ald2ydx`. Python-пакет внутри дерева кода называется `ald2ydx`
(запуск: `python -m ald2ydx`).

## 0. Требования
- Python **3.9+** (код использует `from __future__ import annotations`, проверено на 3.11).
  В Astra 1.7.x в репозитории «Обновления» есть `python3` 3.9/3.11; в 1.8 — 3.11+.
- Сетевой доступ сервера к ALD Pro (`https://<ald-pro-host>:443`) и к
  `cloud-api.yandex.net` / `api360.yandex.net` (443).
- Сервисная УЗ ALD Pro с правами чтения каталога; OAuth-токен Яндекс 360 с правами Directory API.
- Если используется мандатный контроль целостности (ПАРТОЛ/МКИ) — размещайте код в зоне,
  где запись разрешена сервисному пользователю, либо управляйте правами штатными средствами (`fly-*`);
  обычные `chmod/chown` также работают.

## 1. Установка системных пакетов
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ca-certificates rsync
python3 --version   # >= 3.9
```

## 2. Создание сервисного пользователя и каталогов
```bash
sudo useradd -r -m -d /var/lib/ald2ydx -s /usr/sbin/nologin ald2ydx
sudo mkdir -p /opt/ya360-aldpro_syncer /etc/ald2ydx /var/log/ald2ydx /var/lib/ald2ydx
```

## 3. Развёртывание кода в /opt/ya360-aldpro_syncer
Скопируйте репозиторий (git clone / scp / rsync) на сервер, затем:
```bash
sudo cp -r ald2ydx requirements.txt deploy config /opt/ya360-aldpro_syncer/
sudo chown -R root:ald2ydx /opt/ya360-aldpro_syncer && sudo chmod -R g-w,o-rwx /opt/ya360-aldpro_syncer

# виртуальное окружение внутри дерева кода
sudo -u ald2ydx python3 -m venv /opt/ya360-aldpro_syncer/venv
sudo /opt/ya360-aldpro_syncer/venv/bin/pip install --no-cache-dir \
    -r /opt/ya360-aldpro_syncer/requirements.txt
# Для air-gapped: скачайте колёса на машине с интернетом
#   pip download -r requirements.txt -d wheels/
# перенесите wheels/ и поставьте:
#   pip install --no-index --find-links wheels/ httpx PyYAML pydantic
```

## 4. Конфигурация
```bash
sudo cp /opt/ya360-aldpro_syncer/config/config.example.yaml /etc/ald2ydx/config.yaml
sudoedit /etc/ald2ydx/config.yaml   # base_url, org_id, base_dn, root_department_id, state_path, api_host
sudo cp /opt/ya360-aldpro_syncer/deploy/secret.env.example /etc/ald2ydx/secret.env
sudoedit /etc/ald2ydx/secret.env    # пароли/токены
sudo chmod 600 /etc/ald2ydx/secret.env
sudo chown root:ald2ydx /etc/ald2ydx/secret.env
sudo chown -R ald2ydx:ald2ydx /var/lib/ald2ydx /var/log/ald2ydx
```
Секреты задаются переменными окружения (переопределяют YAML):
`A2Y_ALD_PRO_PASSWORD`, `A2Y_YANDEX360_OAUTH_TOKEN`, `A2Y_YANDEX360_INITIAL_PASSWORD`.
Примечание: `A2Y_YANDEX360_INITIAL_PASSWORD` обязателен — `UserService_Create` требует поле `password`.

## 5. Проверка вручную (dry-run, ничего не меняет в Яндекс 360)
```bash
cd /opt/ya360-aldpro_syncer
sudo -u ald2ydx env A2Y_CONFIG=/etc/ald2ydx/config.yaml \
    /opt/ya360-aldpro_syncer/venv/bin/python -m ald2ydx --dry-run --mode full
echo $?   # 0 — успех, 1 — есть ошибки синхронизации, 2 — ошибка конфигурации
```
При внутреннем самоподписанном сертификате ALD Pro укажите в конфиге
`ald_pro.verify_ssl: /etc/ssl/certs/aldpro-ca.pem`.

## 6. Боевой прогон вручную
```bash
cd /opt/ya360-aldpro_syncer
sudo -u ald2ydx env A2Y_CONFIG=/etc/ald2ydx/config.yaml \
    /opt/ya360-aldpro_syncer/venv/bin/python -m ald2ydx --mode full
```
Первый прогон делайте в режиме `full` — он создаёт файл состояния `sync.state_path`
для последующих инкрементальных прогонов.

## 7. Запуск по расписанию (systemd timer)
```bash
sudo cp /opt/ya360-aldpro_syncer/deploy/systemd/ald2ydx.service \
        /opt/ya360-aldpro_syncer/deploy/systemd/ald2ydx.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ald2ydx.timer
systemctl list-timers | grep ald2ydx
```
Однократный запуск: `sudo systemctl start ald2ydx.service`
Логи: `journalctl -u ald2ydx.service -f` и `/var/log/ald2ydx/sync.log`.

## 8. Настройка расписания
Интервал задаётся в `/etc/systemd/system/ald2ydx.timer` параметром `OnUnitActiveSec=`
(по умолчанию 1h; после правки — `sudo systemctl daemon-reload`).
Для cron вместо timer:
```cron
# crontab -e для пользователя ald2ydx
0 * * * * cd /opt/ya360-aldpro_syncer && set -a && . /etc/ald2ydx/secret.env && set +a && \
  A2Y_CONFIG=/etc/ald2ydx/config.yaml /opt/ya360-aldpro_syncer/venv/bin/python -m ald2ydx \
  >> /var/log/ald2ydx/cron.log 2>&1
```

## 9. Обновление версии
```bash
sudo rsync -a --delete ./ald2ydx/ /opt/ya360-aldpro_syncer/ald2ydx/   # только пакет кода; venv и конфиги не трогаем
sudo /opt/ya360-aldpro_syncer/venv/bin/pip install -r /opt/ya360-aldpro_syncer/requirements.txt
sudo systemctl restart ald2ydx.timer
```

## 10. Откат / экстренная остановка
```bash
sudo systemctl stop ald2ydx.timer      # остановить расписание
# безопасный режим: dry_run: true в /etc/ald2ydx/config.yaml — модуль читает оба каталога, но не пишет в Яндекс 360
```

## 11. Диагностика типовых проблем
| Симптом | Причина/решение |
|---|---|
| `Ошибка загрузки конфигурации` (rc=2) | Не задан обязательный параметр (org_id, base_dn и т.п.) — см. сообщения pydantic |
| 401 от ALD Pro (`POST /api/ds/login`) | Неверные учётные данные сервисной УЗ; проверьте блокировку УЗ в самом ALD |
| 403 `OAuth token ...` от Яндекс 360 | Токен просрочен/не имеет нужных прав организации; перевыпустите токен |
| SSL errors | Добавьте CA в доверенные (`update-ca-certificates`) или `verify_ssl: <путь к pem>` |
| Пустой отчёт при incremental | Проверьте `sync.state_path`: файл доступен на запись пользователю `ald2ydx` |
| Нет удалений сотрудников | В API Яндекс 360 нет метода удаления пользователя — используются `block`/`dismiss` (`on_removed_user`) |
