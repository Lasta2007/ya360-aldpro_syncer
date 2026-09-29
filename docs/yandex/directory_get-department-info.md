---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/directory/get-department-info.md
  - href: https://yandex.ru/dev/api360/doc/ru/directory/get-department-info.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
sourcePath: docs/dev/api360/concepts/gw/directory/get-department-info.md
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

# Получить информацию о подразделении

Возвращает информацию о подразделении по его идентификатору. В ответ не включается список участников подразделения. Чтобы посмотреть эту информацию, воспользуйтесь запросом [Посмотреть информацю о подразделении](../DepartmentService/DepartmentService_Get) на хост `api360.yandex.net`.

{% note info "" %}

Чтобы выполнить запрос, приложению требуется одно из разрешений:

- `directory:read_departments` — просмотр данных подразделений;
- `directory:write_departments` — просмотр и изменение данных подразделений.

{% endnote %}

## Запрос {#request}

##GET## `https://cloud-api.yandex.net/v1/directory/organizations/{org_id}/departments/{department_id}`

### Path-параметры {#path-parameters}

#|
|| **Имя параметра** | **Тип** | **Описание** ||
|| org_id&nbsp;**\*** | integer | Идентификатор организации. ||
|| department_id&nbsp;**\*** | integer | Идентификатор подразделения. ||
|#


### Заголовки {#headers}

```json
Authorization: OAuth <токен>
```

### Пример {#example}

{% cut "Пример запроса" %}

```bash
curl -X GET -H "Authorization: OAuth <токен>" "https://cloud-api.yandex.net/v1/directory/organizations/1/departments/2"
```

{% endcut %}

## Ответ {#response}

### Успешный ответ {#successful}

Результатом корректного запроса является ответ с кодом 200 и телом в формате JSON, где содержится объект с информацией о подразделении.

`200 OK` — запрос выполнен успешно.

<!-- source: ru/_includes/department-info.md -->
#|
|| **Поле** | **Тип** | **Описание** ||
|| aliases | string[] | Алиасы почтовых рассылок. ||
|| created_at | string\<date-time\> | Дата и время создания подразделения. ||
|| description | string | Описание подразделения. ||
|| email | string | Адрес почтовой рассылки подразделения. ||
|| id | integer\<int64\> | Идентификатор подразделения. ||
|| label | string | Имя почтовой рассылки подразделения. Например, для адреса `new-department@ваш-домен.ru` имя почтовой рассылки — это `new-department`. ||
|| members_count | integer\<int64\> | Количество сотрудников подразделения с учетом вложенных подразделений. ||
|| name | string | Название подразделения. ||
|| removed | boolean | Признак удаленного подразделения:

- `true` — подразделение удалено;
- `false` — подразделение действующее. ||
|| parent_id | integer\<int64\> | Идентификатор родительского подразделения. ||
|| is_2fa_enabled | boolean | _В разработке_ 

Статус обязательной двухфакторной аутентификации для подразделения:

- `false` — выключена (по умолчанию);
- `true` — включена. ||
|#



<!-- endsource: ru/_includes/department-info.md -->

#### Пример {#response-example}

{% cut "Пример ответа" %}

```json
{
  "limit": 0,
  "offset": 0,
  "total": 0,
  "items": [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "label": "string",
      "members_count": 0,
      "email": "string",
      "aliases": [
        "string"
      ],
      "removed": true,
      "parent": {
        "id": 0
      },
      "created_at": "string",
      "is_2fa_enabled": false
    }
  ]
}
```

{% endcut %}

### Неуспешный ответ {#unsuccessful}

Ошибки могут быть со следующими HTTP-статусами:

- `400 Bad Request` — параметры запроса не заданы или заданы неверно;
- `401 Unauthorized` — пользователь не авторизован;
- `403 Forbidden` — у пользователя или приложения нет прав на доступ к списку пользователей;
- `404 Not Found` — запрашиваемая организация или подразделение не найдены;
- `500 Internal Server Error` — ошибка произошла на стороне сервера (в этом случае попробуйте повторно отправить запрос через некоторое время).


