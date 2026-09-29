---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_List.md
  - href: https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_List.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

<div class="openapi">

# Просмотреть список

<!-- markdownlint-disable-file -->

{% note warning "Метод устарел и не поддерживается" %}

Используйте новый метод [Получить список сотрудников организации](https://yandex.ru/dev/api360/doc/ru/directory/get-users.md).

{% endnote %}

Возвращает список сотрудников с постраничной навигацией.

{% note info %}

Требуется разрешение на чтение данных сотрудников.

{% endnote %}

## Request

<div class="openapi__requests">

<div class="openapi__request__wrapper" style="--method: var(--dc-openapi-methods-get);margin-bottom: 12px">

<div class="openapi__request">

GET {.openapi__method}
```text translate=no
https://api360.yandex.net/directory/v1/org/{orgId}/users
```

</div>

</div>

</div>

### Path parameters

#|
|| **Name** | **Description** ||
||

_orgId_{.json-schema-reset .json-schema-property .json-schema-required}
{.table-cell}|
**Type**: integer

Идентификатор организации.
{.table-cell}
||
|#{.json-schema-properties}

### Query parameters

#|
|| **Name** | **Description** ||
||

_page_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Номер страницы ответа. Значение по умолчанию — `1`.
{.table-cell}
||
||

_perPage_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Количество сотрудников на одной странице ответа. Значение по умолчанию — `10`. Максимальное значение — `1000`.
{.table-cell}
||
|#{.json-schema-properties}

## Responses

<div class="openapi__response__code__200">

## 200 OK

`200 OK` — запрос выполнен успешно.

<div class="openapi-entity">

### Body

{% cut "application/json" %}

```json translate=no
{
  "users": [
    {
      "id": "example",
      "nickname": "example",
      "departmentId": 0,
      "email": "example",
      "name": {
        "first": "example",
        "last": "example",
        "middle": "example"
      },
      "gender": "example",
      "position": "example",
      "avatarId": "example",
      "about": "example",
      "birthday": "example",
      "contacts": [
        {
          "type": "example",
          "value": "example",
          "main": true,
          "alias": true,
          "synthetic": true,
          "label": "example"
        }
      ],
      "aliases": [
        "example"
      ],
      "groups": [
        0
      ],
      "externalId": "example",
      "isAdmin": true,
      "isRobot": true,
      "isDismissed": true,
      "isEnabled": true,
      "isEnabledUpdatedAt": "2025-01-01T00:00:00Z",
      "timezone": "example",
      "language": "example",
      "createdAt": "2025-01-01T00:00:00Z",
      "updatedAt": "2025-01-01T00:00:00Z"
    }
  ],
  "page": 0,
  "pages": 0,
  "perPage": 0,
  "total": 0
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_page_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Номер страницы ответа.
{.table-cell}
||
||

_pages_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Количество страниц ответа.
{.table-cell}
||
||

_perPage_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Количество сотрудников на одной странице ответа.
{.table-cell}
||
||

_total_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Общее количество сотрудников.
{.table-cell}
||
||

_users_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [v1User](#entity-v1User)[]

Список сотрудников.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "id": "example",
    "nickname": "example",
    "departmentId": 0,
    "email": "example",
    "name": {
      "first": "example",
      "last": "example",
      "middle": "example"
    },
    "gender": "example",
    "position": "example",
    "avatarId": "example",
    "about": "example",
    "birthday": "example",
    "contacts": [
      {
        "type": "example",
        "value": "example",
        "main": true,
        "alias": true,
        "synthetic": true,
        "label": "example"
      }
    ],
    "aliases": [
      "example"
    ],
    "groups": [
      0
    ],
    "externalId": "example",
    "isAdmin": true,
    "isRobot": true,
    "isDismissed": true,
    "isEnabled": true,
    "isEnabledUpdatedAt": "2025-01-01T00:00:00Z",
    "timezone": "example",
    "language": "example",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  }
]
```

{% endcut %}
{.table-cell}
||
|#{.json-schema-properties}

</div>

<div class="openapi-entity">

### v1UserName {#entity-v1UserName}

ФИО сотрудника.

#|
|| **Name** | **Description** ||
||

_first_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Имя сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_last_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Фамилия сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_middle_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Отчество сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
{
  "first": "example",
  "last": "example",
  "middle": "example"
}
```

{% endcut %}

</div>

<div class="openapi-entity">

### v1UserContact {#entity-v1UserContact}

Контакты сотрудника.

#|
|| **Name** | **Description** ||
||

_alias_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Если у сотрудника есть алиас, для него автоматически создается контакт типа `email`:

- `true` — контакт создан на основе алиаса;
- `false` — контакт создан вручную.

{.table-cell}
||
||

_label_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Произвольная метка контакта.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_main_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Признак основного контакта:

- `true` — основной;
- `false` — альтернативный.

{.table-cell}
||
||

_synthetic_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Признак автоматически созданного контакта:

- `true` — контакт создан автоматически;
- `false` — контакт создан вручную.

{.table-cell}
||
||

_type_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Тип контакта.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_value_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Значение контакта.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
{
  "type": "example",
  "value": "example",
  "main": true,
  "alias": true,
  "synthetic": true,
  "label": "example"
}
```

{% endcut %}

</div>

<div class="openapi-entity">

### v1User {#entity-v1User}

Сотрудник.

#|
|| **Name** | **Description** ||
||

_about_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_aliases_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string[]

Список алиасов сотрудника.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  "example"
]
```

{% endcut %}
{.table-cell}
||
||

_avatarId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Идентификатор аватара сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_birthday_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Дата рождения сотрудника. В формате `YYYY-MM-DD` или пустая строка.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_contacts_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [v1UserContact](#entity-v1UserContact)[]

Список контактов сотрудника.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "type": "example",
    "value": "example",
    "main": true,
    "alias": true,
    "synthetic": true,
    "label": "example"
  }
]
```

{% endcut %}
{.table-cell}
||
||

_createdAt_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string&lt;date-time&gt;

Дата и время создания сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `2025-01-01T00:00:00Z`
{.table-cell}
||
||

_departmentId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Идентификатор подразделения, в котором состоит сотрудник.
{.table-cell}
||
||

_email_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Основной адрес электронной почты сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_externalId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Произвольный внешний идентификатор сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_gender_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Пол сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_groups_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer[]

Идентификаторы групп, в которых состоит сотрудник.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  0
]
```

{% endcut %}
{.table-cell}
||
||

_id_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string&lt;uint64&gt;

Идентификатор сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_isAdmin_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Признак администратора организации:

- `true` — администратор;
- `false` — рядовой пользователь.

{.table-cell}
||
||

_isDismissed_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Статус сотрудника:

- `true` — уволенный;
- `false` — действующий.

{.table-cell}
||
||

_isEnabled_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Статус аккаунта:

- `true` — активен;
- `false` — заблокирован.

{.table-cell}
||
||

_isEnabledUpdatedAt_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string&lt;date-time&gt;

Дата и время последнего изменения статуса аккаунта сотрудника. Отсутствует если статус никогда не менялся.

_Example:_{.json-schema-reset .json-schema-example} `2025-01-01T00:00:00Z`
{.table-cell}
||
||

_isRobot_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Признак служебного бота:

- `true` — бот;
- `false` — человек.

{.table-cell}
||
||

_language_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Язык сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_name_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [v1UserName](#entity-v1UserName)

ФИО сотрудника.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
{
  "first": "example",
  "last": "example",
  "middle": "example"
}
```

{% endcut %}
{.table-cell}
||
||

_nickname_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Логин сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_position_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Должность сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_timezone_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Часовой пояс сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_updatedAt_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string&lt;date-time&gt;

Дата и время изменения сотрудника.

_Example:_{.json-schema-reset .json-schema-example} `2025-01-01T00:00:00Z`
{.table-cell}
||
|#{.json-schema-properties}

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
{
  "id": "example",
  "nickname": "example",
  "departmentId": 0,
  "email": "example",
  "name": {
    "first": "example",
    "last": "example",
    "middle": "example"
  },
  "gender": "example",
  "position": "example",
  "avatarId": "example",
  "about": "example",
  "birthday": "example",
  "contacts": [
    {
      "type": "example",
      "value": "example",
      "main": true,
      "alias": true,
      "synthetic": true,
      "label": "example"
    }
  ],
  "aliases": [
    "example"
  ],
  "groups": [
    0
  ],
  "externalId": "example",
  "isAdmin": true,
  "isRobot": true,
  "isDismissed": true,
  "isEnabled": true,
  "isEnabledUpdatedAt": "2025-01-01T00:00:00Z",
  "timezone": "example",
  "language": "example",
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-01T00:00:00Z"
}
```

{% endcut %}

</div>

</div>

<div class="openapi__response__code__400">

## 400 Bad Request

`400 Bad Request` — некорректный запрос.

<div class="openapi-entity">

### Body

{% cut "application/json" %}

```json translate=no
{
  "code": 0,
  "message": "example",
  "details": [
    {
      "@type": "example"
    }
  ]
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_code_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Код ошибки.
{.table-cell}
||
||

_details_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [protobufAny](#entity-protobufAny)[]

Дополнительные сведения об ошибке.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "@type": "example"
  }
]
```

{% endcut %}
{.table-cell}
||
||

_message_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание ошибки.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

</div>

<div class="openapi-entity">

### protobufAny {#entity-protobufAny}

#|
|| **Name** | **Description** ||
||

_@type_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_[additional]_{.json-schema-reset .json-schema-additional-property}
{.table-cell}|
**Type**: unknown

_Example:_{.json-schema-reset .json-schema-example} `null`
{.table-cell}
||
|#{.json-schema-properties}

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
{
  "@type": "example"
}
```

{% endcut %}

</div>

</div>

<div class="openapi__response__code__401">

## 401 Unauthorized

`401 Unauthorized` — пользователь не авторизован.

<div class="openapi-entity">

### Body

{% cut "application/json" %}

```json translate=no
{
  "code": 0,
  "message": "example",
  "details": [
    {
      "@type": "example"
    }
  ]
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_code_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Код ошибки.
{.table-cell}
||
||

_details_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [protobufAny](#entity-protobufAny)[]

Дополнительные сведения об ошибке.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "@type": "example"
  }
]
```

{% endcut %}
{.table-cell}
||
||

_message_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание ошибки.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

</div>

</div>

<div class="openapi__response__code__403">

## 403 Forbidden

`403 Forbidden` — у пользователя или приложения нет прав на доступ к ресурсу, запрос отклонен.

<div class="openapi-entity">

### Body

{% cut "application/json" %}

```json translate=no
{
  "code": 0,
  "message": "example",
  "details": [
    {
      "@type": "example"
    }
  ]
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_code_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Код ошибки.
{.table-cell}
||
||

_details_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [protobufAny](#entity-protobufAny)[]

Дополнительные сведения об ошибке.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "@type": "example"
  }
]
```

{% endcut %}
{.table-cell}
||
||

_message_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание ошибки.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

</div>

</div>

<div class="openapi__response__code__404">

## 404 Not Found

`404 Not Found` — запрашиваемый ресурс не найден.

<div class="openapi-entity">

### Body

{% cut "application/json" %}

```json translate=no
{
  "code": 0,
  "message": "example",
  "details": [
    {
      "@type": "example"
    }
  ]
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_code_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Код ошибки.
{.table-cell}
||
||

_details_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [protobufAny](#entity-protobufAny)[]

Дополнительные сведения об ошибке.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "@type": "example"
  }
]
```

{% endcut %}
{.table-cell}
||
||

_message_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание ошибки.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

</div>

</div>

<div class="openapi__response__code__500">

## 500 Internal Server Error

`500 Internal Server Error` — внутренняя ошибка сервиса. Попробуйте повторно отправить запрос через некоторое время.

<div class="openapi-entity">

### Body

{% cut "application/json" %}

```json translate=no
{
  "code": 0,
  "message": "example",
  "details": [
    {
      "@type": "example"
    }
  ]
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_code_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Код ошибки.
{.table-cell}
||
||

_details_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [protobufAny](#entity-protobufAny)[]

Дополнительные сведения об ошибке.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "@type": "example"
  }
]
```

{% endcut %}
{.table-cell}
||
||

_message_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание ошибки.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
|#{.json-schema-properties}

</div>

</div>

</div>

[*Deprecated]: No longer supported, please use an alternative and newer version.