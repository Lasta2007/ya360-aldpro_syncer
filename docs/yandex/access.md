---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/access.md
  - href: https://yandex.ru/dev/api360/doc/ru/access.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
sourcePath: docs/dev/api360/concepts/access.md
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

# Доступ к API


Запросы к API Яндекс 360 можно отправлять на один из двух хостов:

- `https://api360.yandex.net/` — устаревший хост. Поддерживается в полном объеме, но методы на нем больше не обновляются.
- `https://cloud-api.yandex.net/` — актуальный хост. Все новые методы API доступны только на этом хосте.



## Создание OAuth-приложения и получение токена {#new}

Яндекс 360 для бизнеса авторизует приложения с помощью [OAuth-токенов](https://yandex.ru/dev/id/doc/ru/concepts/ya-oauth-intro). Чтобы использовать протокол OAuth при работе с Яндекс 360:

1. Создайте свое OAuth-приложение по [инструкции](https://yandex.ru/dev/id/doc/ru/register-api) из Справки OAuth Яндекс ID. В разделе **Доступ к данным** укажите необходимые права доступа из тех, которые используются в API Яндекс 360 для бизнеса:

   **Яндекс 360 Directory API**

   * Чтение данных об организациях — `directory:read_organization`;
   * Редактирование организации — `directory:write_organization`;
   * Чтение данных о подразделениях — `directory:read_departments`;
   * Управление подразделениями — `directory:write_departments`;
   * Чтение данных о группах — `directory:read_groups`;
   * Управление группами — `directory:write_groups`;
   * Чтение данных о сотрудниках — `directory:read_users`;
   * Управление сотрудниками — `directory:write_users`;
   * Чтение данных о доменах организации — `directory:read_domains`;
   * Управление доменами организации — `directory:write_domains`;
   * Управление DNS-записями — `directory:manage_dns`;
   * Чтение данных об офисах организации — `directory:read_offices`;
   * Управление офисами организации — `directory:write_offices`;
   * Чтение данных о переговорках организации — `directory:read_rooms`;
   * Управление переговорками организации — `directory:write_rooms`.

   **Яндекс 360 Admin API**

   * Чтение настроек антиспама для организации — `ya360_admin:mail_read_antispam_settings`;
   * Управление настройками антиспама для организации — `ya360_admin:mail_write_antispam_settings`;
   * Чтение настроек почты пользователя — `ya360_admin:mail_read_user_settings`;
   * Управление настройками почты пользователя — `ya360_admin:mail_write_user_settings`;
   * Чтение правил обработки почты для домена — `ya360_admin:mail_read_routing_rules`;
   * Управление правилами обработки почты для домена — `ya360_admin:mail_write_routing_rules`;
   * Чтение правил маршрутизации организации — `ya360_admin:mail_read_domain_routes`;
   * Управление правилами маршрутизации организации — `ya360_admin:mail_write_domain_routes`;
   * Чтение информации о правах доступа к почтовым ящикам — `ya360_admin:mail_read_shared_mailbox_inventory`;
   * Управление правами доступа к почтовым ящикам — `ya360_admin:mail_write_shared_mailbox_inventory`;
   * Чтение настроек почты организации — `ya360_admin:mail_read_organization_settings`;
   * Управление настройками почты организации — `ya360_admin:mail_write_organization_settings`.
   * Просмотр разрешений на рассылку — `ya360_admin:mail_read_mail_list_permissions`;
   * Изменение разрешений на рассылку — `ya360_admin:mail_write_mail_list_permissions`.

   **Яндекс 360 Security API**

   * Управление обязательной 2FA для пользователей — `ya360_security:domain_2fa_write`;
   * Чтение информации о настройках cookie сессий пользователей — `ya360_security:domain_sessions_read`;
   * Управление настройками и авторизационными cookie сессиями пользователей — `ya360_security:domain_sessions_write`;
   * Чтение информации о параметрах паролей пользователей — `ya360_security:domain_passwords_read`;
   * Управление параметрами паролей пользователей — `ya360_security:domain_passwords_write`;
   * Чтение информации о настройках безопасности организации — `ya360_security:domain_settings_read`;
   * Управление настройками безопасности организации — `ya360_security:domain_settings_write`;
   * Чтение списка сервисных приложений — `ya360_security:service_applications_read`;
   * Управление списком сервисных приложений — `ya360_security:service_applications_write`;
   * Чтение событий аудит-лога Диска — `ya360_security:audit_log_disk`;
   * Чтение событий аудит-лога Почты — `ya360_security:audit_log_mail`;
   * Чтение событий аудит-лога организации — `ya360_security:read_auditlog`.

1. На странице приложения скопируйте идентификатор приложения из поля **ClientID** — он потребуется для получения OAuth-токена. В дальнейшем открыть страницу со всеми вашими приложениями вы сможете по ссылке [oauth.yandex.ru](https://oauth.yandex.ru).



1. Получите OAuth-токен: {#token}

   1. Перейдите по ссылке

      ```html
      https://oauth.yandex.ru/authorize?response_type=token&client_id=<идентификатор_приложения>
      ```

      Вместо `<идентификатор_приложения>` подставьте значение **ClientID**.

   1. Если токен вашему приложению выдается впервые или срок жизни предыдущего токена истек, откроется экран авторизации. Войдите в сервис.
   1. Скопируйте значение токена с открывшейся страницы и сохраните его.

      {% note info "Вы не сможете найти полученный токен в личном кабинете" %}

      Сервис Яндекс OAuth не хранит выдаваемые токены в публичном доступе. Если вы не сохранили токен, вы можете получить его еще раз.

      {% endnote %}

   Полученный токен следует передавать в HTTP-заголовке `Authorization` при каждом вызове API, указывая тип токена перед его значением:

   ```bash
   --header 'Authorization: OAuth <OAuth-токен>'
   ```

Полную информацию об OAuth-авторизации и токенах читайте в [документации OAuth-сервиса Яндекса](https://yandex.ru/dev/id/doc/ru/).

## Добавление прав доступа в существующее приложение {#add}

Если у вас уже есть OAuth-приложение для работы с API Яндекс 360 для бизнеса, но у приложение недостаточно прав для осуществления какого-либо запроса, вы можете изменить список доступов:

1. [Авторизуйтесь на Яндексе](https://passport.yandex.ru). Укажите логин и пароль администратора организации, от имени которого создано OAuth-приложение.
2. Откройте страницу [Ваши приложения](https://oauth.yandex.ru) сервиса Яндекс OAuth.
3. Выберите приложение, которое создано для работы с API Яндекс 360 для бизнеса.
4. На странице приложения в разделе **Управление приложением** нажмите **Настройки**.
5. Дополните список доступов теми правами, которые хотите добавить. Чтобы удалить лишнее право, нажмите значок с корзиной напротив него.
6. Нажмите **Сохранить** внизу страницы и подтвердите сохранение.

{% note warning "Измененный список доступов будет доступен только с новым токеном" %}

Получите его по [инструкции из п.3.1 выше](#token).

{% endnote %}

