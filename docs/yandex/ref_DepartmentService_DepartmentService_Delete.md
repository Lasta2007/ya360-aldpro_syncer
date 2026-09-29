---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/ref/DepartmentService/DepartmentService_Delete.md
  - href: https://yandex.ru/dev/api360/doc/ru/ref/DepartmentService/DepartmentService_Delete.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

<div class="openapi">

# Удалить подразделение

<!-- markdownlint-disable-file -->

Удаляет подразделение. Запрос может быть выполнен только для подразделения без сотрудников и вложенных подразделений.

{% note info %}

Требуется разрешение на изменение данных подразделений.

{% endnote %}

## Request

<div class="openapi__requests">

<div class="openapi__request__wrapper" style="--method: var(--dc-openapi-methods-delete);margin-bottom: 12px">

<div class="openapi__request">

DELETE {.openapi__method}
```text translate=no
https://api360.yandex.net/directory/v1/org/{orgId}/departments/{departmentId}
```

</div>

</div>

</div>

### Path parameters

#|
|| **Name** | **Description** ||
||

_departmentId_{.json-schema-reset .json-schema-property .json-schema-required}
{.table-cell}|
**Type**: integer

Идентификатор подразделения.
{.table-cell}
||
||

_orgId_{.json-schema-reset .json-schema-property .json-schema-required}
{.table-cell}|
**Type**: integer

Идентификатор организации.
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
  "id": 0,
  "removed": true
}
```

{% endcut %}

#|
|| **Name** | **Description** ||
||

_id_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: integer

Идентификатор подразделения.
{.table-cell}
||
||

_removed_{.json-schema-reset .json-schema-property}
{.table-cell}|
**Type**: boolean

Признак удаления:

- `true` — удалено;
- `false` — не удалено.

{.table-cell}
||
|#{.json-schema-properties}

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