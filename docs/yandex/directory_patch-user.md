---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/directory/patch-user.md
  - href: https://yandex.ru/dev/api360/doc/ru/directory/patch-user.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
sourcePath: docs/dev/api360/concepts/gw/directory/patch-user.md
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

# Изменить параметры сотрудника организации

Изменяет адрес электронной почты для отправки писем по умолчанию и отображаемое имя сотрудника организации. Чтобы изменить остальные параметры, воспользуйтесь запросом [Изменить информацию](https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_Update.md) на хост `api360.yandex.net`.

{% note info "" %}

Чтобы выполнить запрос, приложению требуется одно из разрешений:

- `directory:read_users` — просмотр данных пользователей;
- `directory:write_users` — просмотр и изменение данных пользователей.

{% endnote %}

## Запрос {#request}

##PATCH## `https://cloud-api.yandex.net/v1/directory/organizations/{org_id}/users/{user_id}`

### Path-параметры {#path-parameters}

#|
|| **Имя параметра** | **Тип** | **Описание** ||
|| org_id&nbsp;**\*** | integer | Идентификатор организации. ||
|| user_id&nbsp;**\*** | string\<uint64\> | Идентификатор сотрудника. ||
|#

### Заголовки {#headers}

```json
Authorization: OAuth <токен>
Content-Type: application/json
```


### Тело {#body}

#|
|| **Имя параметра** | **Тип** | **Описание** ||
|| default_email | string | Адрес электронной почты сотрудника для рабочей переписки по умолчанию. ||
|| display_name | string | Отображаемое имя сотрудника. ||
|#

### Пример {#example}

{% cut "Пример запроса" %}

```bash
curl --request PATCH \
  --url https://cloud-api.yandex.net/v1/directory/organizations/167730/users/1130000007986051 \
  --header 'authorization: OAuth <токен>' \
  --header 'content-type: application/json' \
  --data '{
  "default_email": "test@company.ru", 
  "display_name": "tester"
}'
```

{% endcut %}

## Ответ {#response}

### Успешный ответ {#successful}

Результатом корректного запроса является ответ с кодом 200 и телом в формате JSON, где содержится объект с информацией о сотруднике.

`200 OK` — запрос выполнен успешно.

#|
|| **Поле** | **Тип** | **Описание** ||
|| about | string | Описание сотрудника. ||
|| aliases | string[] | Список алиасов сотрудника. ||
|| avatar_id | string | Идентификатор аватара сотрудника. ||
|| birthday | string | Дата рождения сотрудника.

Формат: `YYYY-MM-DD`. Может быть пустой строкой. ||
|| contacts | [v1UserContact](#v1usercontact)[] | Список контактов сотрудника. ||
|| created_at | string\<date-time\> | Дата и время создания сотрудника. ||
|| department_id | integer\<int64\> | Идентификатор подразделения сотрудника. ||
|| email | string | Адрес электронной почты сотрудника на основном домене организации. ||
|| default_email | string | Адрес электронной почты сотрудника для рабочей переписки по умолчанию. ||
|| external_id | string | Произвольный внешний идентификатор. ||
|| gender | string | Пол сотрудника. ||
|| groups | integer\<int64\>[] | Идентификаторы групп сотрудника. ||
|| id | string\<uint64\> | Идентификатор сотрудника. ||
|| is_2fa_enabled | boolean | Статус обязательной персональной двухфакторной аутентификации:

- `true` — включена;
- `false` — выключена. ||
|| is_admin | boolean | Признак администратора организации:

- `true` — администратор;
- `false` — рядовой пользователь. ||
|| is_dismissed | boolean | Статус сотрудника:

- `true` — уволенный;
- `false` — действующий. ||
|| is_enabled | boolean | Статус аккаунта:

- `true` — активен;
- `false` — заблокирован. ||
|| is_enabled_updated_at | string\<date-time\> | Дата и время последнего изменения статуса аккаунта. Отсутствует, если статус никогда не менялся. ||
|| is_robot | boolean | Признак служебного бота:

- `true` — бот;
- `false` — человек. ||
|| language | string | Язык сотрудника. ||
|| name | [v1UserName](#v1username) | ФИО сотрудника. ||
|| display_name | string | Отображаемое имя сотрудника. ||
|| nickname | string | Логин сотрудника. ||
|| position | string | Должность сотрудника. ||
|| timezone | string | Часовой пояс сотрудника. ||
|| updated_at | string\<date-time\> | Дата и время изменения данных сотрудника. ||
|#

#### v1UserContact

#|
|| **Поле** | **Тип** | **Описание** ||
|| alias | boolean | Признак алиаса:

- `true` — контакт создан на основе алиаса;
- `false` — контакт создан вручную. ||
|| label | string | Произвольная метка контакта. ||
|| main | boolean | Признак основного контакта:

- `true` — основной;
- `false` — альтернативный. ||
|| synthetic | boolean | Признак автоматически созданного контакта:

- `true` — контакт создан автоматически;
- `false` — контакт создан вручную. ||
|| type | string | Тип контакта. ||
|| value | string | Значение контакта. ||
|#

#### v1UserName

#|
|| **Поле** | **Тип** | **Описание** ||
|| first | string | Имя сотрудника. ||
|| middle | string | Отчество сотрудника. ||
|| last | string | Фамилия сотрудника. ||
|#

#### Пример {#response-example}

{% cut "Пример ответа" %}

```json
{
  "id": 1130000007986051,
  "nickname": "test",
  "department_id": 1,
  "email": "test@company.ru",
  "default_email": "test@company.ru",
  "name": {
    "first": "test",
    "middle": "test",
    "last": "test"
  },
  "display_name": "tester",
  "gender": "",
  "position": "",
  "avatar_id": "",
  "about": "",
  "birthday": "",
  "contacts": [
    {
      "type": "email",
      "value": "test-company",
      "main": false,
      "alias": false,
      "synthetic": false
    },
    {
      "type": "email",
      "value": "test@company.ru",
      "main": true,
      "alias": false,
      "synthetic": true
    },
  ],
  "aliases": [],
  "external_id": "",
  "is_admin": false,
  "is_robot": false,
  "is_dismissed": false,
  "is_2fa_enabled": false,
  "is_enabled": true,
  "timezone": "Europe/Moscow",
  "language": "ru",
  "created_at": "2026-02-26T12:29:38.659354Z",
  "updated_at": "2026-02-26T15:29:38.659354+03:00"
}
```

{% endcut %}

### Неуспешный ответ {#unsuccessful}

Ошибки могут быть со следующими HTTP-статусами:

- `400 Bad Request` — параметры запроса не заданы или заданы неверно;
- `401 Unauthorized` — пользователь не авторизован;
- `403 Forbidden` — у пользователя или приложения нет прав на доступ к списку пользователей;
- `404 Not Found` — запрашиваемая организация не найдена;
- `500 Internal Server Error` — ошибка произошла на стороне сервера (в этом случае попробуйте повторно отправить запрос через некоторое время).


