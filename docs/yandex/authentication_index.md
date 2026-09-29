---
metadata:
  - name: generator
    content: Diplodoc Platform v5.61.1
alternate:
  - https://yandex.ru/dev/api360/doc/ru/authentication/index.md
  - href: https://yandex.ru/dev/api360/doc/ru/authentication/index.md
    type: text/markdown
    title: Markdown version
  - href: https://yandex.ru/dev/api360/doc/ru/llms.txt
    rel: describedby
sourcePath: docs/dev/api360/concepts/gw/authentication/index.md
---
> **Documentation Index:** Fetch the complete configuration index at https://yandex.ru/dev/api360/doc/ru/llms.txt

# Двухфакторная аутентификация с возможностью персональной настройки

Сервис для управления обязательной двухфакторной аутентификацией (2FA) с возможностью ее настройки как сразу для всех пользователей с аккаунтами на домене организации (режим `per_domain`), так и выборочно для отдельных сотрудников (режим `per_user`).


{% note tip "" %}

Этот инструмент доступен в тарифах для крупных организаций **Корпоративный + Безопасность** и **Корпоративный Максимум**. Чтобы узнать подробности, оставьте заявку: менеджер Яндекс 360 свяжется с вами, ответит на все вопросы и поможет с подключением. [Оставить заявку](https://forms.yandex.ru/surveys/13738802.99a3500a5b3c9b59ead425e5c11155ed6b45516d/)

{% endnote %}


{% cut "Что будет при смене режима 2FA с `per_domain` на `per_user`" %}

* У пользователей, которые самостоятельно включали себе двухфакторную аутентификацию еще до настройки принудительной 2FA в режиме `per_domain`, она останется включенной.
* У остальных пользователей двухфакторная аутентификация будет выключена.

В режиме `per_user` пользователи могут самостоятельно включать и выключать себе 2FA в настройках безопасности Яндекс ID.

{% endcut %}


Права доступа, необходимые приложению для работы с двухфакторной аутентификацией:

* `ya360_security:domain_2fa_write` — управление обязательной двухфакторной аутентификацией для пользователей.


## Endpoints

* [Посмотреть статус 2FA](https://yandex.ru/dev/api360/doc/ru/authentication/get-2fa.md)
* [Изменить статус 2FA](https://yandex.ru/dev/api360/doc/ru/authentication/put-2fa.md)
* [Закрыть сессии всех пользователей](https://yandex.ru/dev/api360/doc/ru/authentication/post-2fa.md)
