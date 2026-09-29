# Развёртывание ya360-aldpro_syncer на Astra Linux (Смоленск/Воронеж, 1.7–1.8)

**Весь проект размещается в одном каталоге: `/opt/ya360-aldpro_syncer`.**
Никаких данных вне него: конфиг, секреты, venv, состояние и логи — внутри дерева проекта.

Структура каталога после развёртывания:
```text
/opt/ya360-aldpro_syncer/
├── ald2ydx/              # python-пакет (код модуля; запуск: python -m ald2ydx)
├── config/
│   ├── config.example.yaml
│   └── config.yaml       # рабочая конфигурация (создаётся на шаге 4)
├── deploy/               # systemd-юниты, пример secret.env
├── requirements.txt
├── venv/                 # виртуальное окружение (шаг 3)
├── state/                # sync_state.json — состояние инкрементальной синхронизации
├── logs/                 # sync.log
└── secret.env            # секреты, права 600 (шаг 4)
```

## 0. Требования
- Python **3.9+** (в Astra 1.7.x — `python3` 3.9/3.11 из репозитория «Обновления», в 1.8 — 3.11+).
- Сетевой доступ сервера к ALD Pro (`https://<ald-pro-host>:443`) и к
  `cloud-api.yandex.net` / `api360.yandex.net` (443).
- Сервисная УЗ ALD Pro с правами чтения каталога; OAuth-токен Яндекс 360 с правами Directory API.
- Если включён мандатный контроль целостности (ПАРТОЛ/МКИ) — размещайте дерево в зоне,
  где запись сервисному пользователю разрешена, либо управляйте правами штатными средствами (`fly-*`).
- ВНИМАНИЕ: `/opt/ya360-aldpro_syncer` по умолчанию принадлежит root. Команда
  `sudo -u ald2ydx python3 -m venv /opt/ya360-aldpro_syncer/venv` без предварительной смены
  владельца завершится `Permission denied`. Правильный порядок — на шаге 3.

## 1. Установка системных пакетов
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ca-certificates rsync
python3 --version   # >= 3.9
```

## 2. Создание сервисного пользователя
```bash
sudo useradd -r -s /usr/sbin/nologin ald2ydx
```
Домашний каталог сервисному пользователю не создаём — всё рабочее пространство находится
в `/opt/ya360-aldpro_syncer`.

## 3. Развёртывание кода и venv (всё в /opt/ya360-aldpro_syncer)
Скопируйте репозиторий на сервер (git clone / scp / rsync) в `/opt/ya360-aldpro_syncer`, затем:
```bash
# Каталоги для состояния и логов — тоже внутри дерева проекта
sudo mkdir -p /opt/ya360-aldpro_syncer/state /opt/ya360-aldpro_syncer/logs /opt/ya360-aldpro_syncer/config

# Права: код принадлежит root (защита от подмены), группа ald2ydx;
# запись нужна только сервисному пользователю в state/, logs/ и при сборке venv.
sudo chown -R root:ald2ydx /opt/ya360-aldpro_syncer
sudo chmod -R o-rwx /opt/ya360-aldpro_syncer
sudo chown -R ald2ydx:ald2ydx /opt/ya360-aldpro_syncer/state /opt/ya360-aldpro_syncer/logs

# Виртуальное окружение ВНУТРИ дерева проекта (от root, затем отдать сервисному пользователю):
sudo python3 -m venv /opt/ya360-aldpro_syncer/venv
sudo chown -R ald2ydx:ald2ydx /opt/ya360-aldpro_syncer/venv

sudo /opt/ya360-aldpro_syncer/venv/bin/pip install --no-cache-dir \
    -r /opt/ya360-aldpro_syncer/requirements.txt
# Для air-gapped контура: на машине с интернетом — pip download -r requirements.txt -d wheels/,
# перенести wheels/ в /opt/ya360-aldpro_syncer/ и:
#   /opt/ya360-aldpro_syncer/venv/bin/pip install --no-index --find-links /opt/ya360-aldpro_syncer/wheels httpx PyYAML pydantic
```

## 4. Конфигурация и секреты (внутри дерева проекта)
```bash
sudo cp /opt/ya360-aldpro_syncer/config/config.example.yaml /opt/ya360-aldpro_syncer/config/config.yaml
sudoedit /opt/ya360-aldpro_syncer/config/config.yaml
# обязательно: ald_pro.base_url/login, yandex360.org_id/api_host,
#   sync.base_dn, sync.root_department_id,
#   sync.state_path = "/opt/ya360-aldpro_syncer/state/sync_state.json"
#   logging.file    = "/opt/ya360-aldpro_syncer/logs/sync.log"

sudo cp /opt/ya360-aldpro_syncer/deploy/secret.env.example /opt/ya360-aldpro_syncer/secret.env
sudoedit /opt/ya360-aldpro_syncer/secret.env      # пароли/токены
sudo chmod 600 /opt/ya360-aldpro_syncer/secret.env
sudo chown ald2ydx:ald2ydx /opt/ya360-aldpro_syncer/secret.env
```
Секреты задаются переменными окружения (переопределяют YAML):
`A2Y_ALD_PRO_PASSWORD`, `A2Y_YANDEX360_OAUTH_TOKEN`, `A2Y_YANDEX360_INITIAL_PASSWORD`.
Примечание: `A2Y_YANDEX360_INITIAL_PASSWORD` обязателен — `UserService_Create` требует поле `password`.
При внутреннем самоподписанном сертификате ALD Pro укажите `ald_pro.verify_ssl: /etc/ssl/certs/aldpro-ca.pem`
(CA-сертификат — единственный допустимый внешний файл; его можно также положить в дерево проекта
и сослаться относительным путём от `/opt/ya360-aldpro_syncer`).

## 5. Проверка вручную (dry-run, ничего не меняет в Яндекс 360)
```bash
sudo -u ald2ydx bash -c 'cd /opt/ya360-aldpro_syncer && set -a && . ./secret.env && set +a && \
    ./venv/bin/python -m ald2ydx --config config/config.yaml --dry-run --mode full'
echo $?   # 0 — успех, 1 — есть ошибки синхронизации, 2 — ошибка конфигурации
```

## 6. Боевой прогон вручную
```bash
sudo -u ald2ydx bash -c 'cd /opt/ya360-aldpro_syncer && set -a && . ./secret.env && set +a && \
    ./venv/bin/python -m ald2ydx --config config/config.yaml --mode full'
```
Первый прогон делайте в режиме `full` — он создаёт `state/sync_state.json`
для последующих инкрементальных прогонов.

## 7. Запуск по расписанию (systemd timer)
```bash
sudo cp /opt/ya360-aldpro_syncer/deploy/systemd/ald2ydx.service \
        /opt/ya360-aldpro_syncer/deploy/systemd/ald2ydx.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ald2ydx.timer
systemctl list-timers | grep ald2ydx
```
Юнит использует пути внутри `/opt/ya360-aldpro_syncer`
(`EnvironmentFile=-/opt/ya360-aldpro_syncer/secret.env`,
`A2Y_CONFIG=/opt/ya360-aldpro_syncer/config/config.yaml`,
`ReadWritePaths=/opt/ya360-aldpro_syncer/state /opt/ya360-aldpro_syncer/logs`).
Однократный запуск: `sudo systemctl start ald2ydx.service`.
Логи: `journalctl -u ald2ydx.service -f` и `/opt/ya360-aldpro_syncer/logs/sync.log`.

## 8. Настройка расписания
Интервал — в `/etc/systemd/system/ald2ydx.timer`, параметр `OnUnitActiveSec=`
(по умолчанию 1h; после правки — `sudo systemctl daemon-reload`).
Альтернатива — cron:
```cron
# crontab -e -u ald2ydx
0 * * * * cd /opt/ya360-aldpro_syncer && set -a && . ./secret.env && set +a && \
  ./venv/bin/python -m ald2ydx --config config/config.yaml >> logs/cron.log 2>&1
```

## 9. Обновление версии
```bash
sudo rsync -a --delete ./ald2ydx/ /opt/ya360-aldpro_syncer/ald2ydx/   # только пакет кода
sudo /opt/ya360-aldpro_syncer/venv/bin/pip install -r /opt/ya360-aldpro_syncer/requirements.txt
sudo systemctl restart ald2ydx.timer
```
`config/config.yaml`, `secret.env`, `state/`, `logs/` и `venv/` при обновлении не затрагиваются.

## 10. Откат / экстренная остановка
```bash
sudo systemctl stop ald2ydx.timer      # остановить расписание
# безопасный режим: dry_run: true в /opt/ya360-aldpro_syncer/config/config.yaml
```

## 11. Диагностика типовых проблем
| Симптом | Причина/решение |
|---|---|
| `Permission denied: '/opt/ya360-aldpro_syncer/venv'` | venv создавался от `ald2ydx` без прав на каталог; создайте от root и отдайте `chown -R ald2ydx:ald2ydx .../venv` (шаг 3) |
| `Ошибка загрузки конфигурации` (rc=2) | Не задан обязательный параметр (org_id, base_dn и т.п.) — см. сообщения pydantic |
| 401 от ALD Pro (`POST /api/ds/login`) | Неверные учётные данные сервисной УЗ; проверьте блокировку УЗ в ALD |
| 403 от Яндекс 360 | OAuth-токен просрочен/без прав Directory API — перевыпустите токен |
| Ошибки SSL | CA-сертификат ALD Pro: `update-ca-certificates` или `verify_ssl: <путь к .pem>` |
| Нет записи состояния | Проверьте права на `/opt/ya360-aldpro_syncer/state` (должен принадлежать `ald2ydx`) |
| Нет удалений сотрудников | В API Яндекс 360 нет метода удаления пользователя — используются `block`/`dismiss` (`sync.on_removed_user`) |

## 12. Полная деинсталляция
Так как весь проект в одном каталоге:
```bash
sudo systemctl disable --now ald2ydx.timer
sudo rm -f /etc/systemd/system/ald2ydx.service /etc/systemd/system/ald2ydx.timer
sudo systemctl daemon-reload
sudo userdel ald2ydx
sudo rm -rf /opt/ya360-aldpro_syncer     # код, конфиг, секреты, состояние, логи — всё здесь
```
