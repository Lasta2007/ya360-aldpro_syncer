---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/ref/DepartmentService/DepartmentService_List.md
  - href: https://yandex.ru/dev/api360/doc/ru/ref/DepartmentService/DepartmentService_List.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

<div class="openapi">

# Посмотреть список подразделений

<!-- markdownlint-disable-file -->

{% note warning "Метод устарел и не поддерживается" %}

Используйте новый метод [Получить список подразделений организации](https://yandex.ru/dev/api360/doc/ru/directory/get-departments.md).

{% endnote %}

Возвращает список подразделений с постраничной навигацией.

{% note info %}

Требуется разрешение на чтение данных подразделений.

{% endnote %}

## Request

<div class="openapi__requests">

<div class="openapi__request__wrapper" style="--method: var(--dc-openapi-methods-get);margin-bottom: 12px">

<div class="openapi__request">

GET {.openapi__method}
```text translate=no
https://api360.yandex.net/directory/v1/org/{orgId}/departments
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

_orderBy_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Вид сортировки.

 - id: По идентификатору.
 - name: По названию.

_Default:_{.json-schema-reset .json-schema-value} `id`

_Enum:_{.json-schema-reset .json-schema-value} `id`, `name`
{.table-cell}
||
||

_page_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Номер страницы ответа. Значение по умолчанию — `1`.
{.table-cell}
||
||

_parentId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Идентификатор родительского подразделения. Если не указан, то выводятся все подразделения организации.
{.table-cell}
||
||

_perPage_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Количество подразделений на одной странице ответа. Значение по умолчанию — `10`.
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
  "departments": [
    {
      "id": 0,
      "name": "example",
      "parentId": 0,
      "description": "example",
      "createdAt": "2025-01-01T00:00:00Z",
      "externalId": "example",
      "label": "example",
      "email": "example",
      "emailId": "example",
      "membersCount": 0,
      "aliases": [
        "example"
      ]
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

_departments_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: [v1Department](#entity-v1Department)[]

Список подразделений.

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
[
  {
    "id": 0,
    "name": "example",
    "parentId": 0,
    "description": "example",
    "createdAt": "2025-01-01T00:00:00Z",
    "externalId": "example",
    "label": "example",
    "email": "example",
    "emailId": "example",
    "membersCount": 0,
    "aliases": [
      "example"
    ]
  }
]
```

{% endcut %}
{.table-cell}
||
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

Количество подразделений на одной странице ответа.
{.table-cell}
||
||

_total_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Общее количество подразделений.
{.table-cell}
||
|#{.json-schema-properties}

</div>

<div class="openapi-entity">

### v1Department {#entity-v1Department}

#|
|| **Name** | **Description** ||
||

_aliases_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string[]

Алиасы почтовых рассылок.

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

_createdAt_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string&lt;date-time&gt;

Дата и время создания подразделения.

_Example:_{.json-schema-reset .json-schema-example} `2025-01-01T00:00:00Z`
{.table-cell}
||
||

_description_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Описание подразделения.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_email_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Адрес почтовой рассылки подразделения.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_emailId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string&lt;uint64&gt;

Идентификатор почтовой рассылки подразделения.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_externalId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Произвольный внешний идентификатор подразделения.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_id_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Идентификатор подразделения.
{.table-cell}
||
||

_label_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Имя почтовой рассылки подразделения. Например, для адреса `new-department@ваш-домен.ru` имя почтовой рассылки — это `new-department`.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_membersCount_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Количество сотрудников подразделения с учетом вложенных подразделений.
{.table-cell}
||
||

_name_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: string

Название подразделения.

_Example:_{.json-schema-reset .json-schema-example} `example`
{.table-cell}
||
||

_parentId_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Идентификатор родительского подразделения.
{.table-cell}
||
|#{.json-schema-properties}

{% cut "**Example**" %}{.json-schema-example}

```json translate=no
{
  "id": 0,
  "name": "example",
  "parentId": 0,
  "description": "example",
  "createdAt": "2025-01-01T00:00:00Z",
  "externalId": "example",
  "label": "example",
  "email": "example",
  "emailId": "example",
  "membersCount": 0,
  "aliases": [
    "example"
  ]
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