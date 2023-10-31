# Пример работы с GigaChat

## Описание

Цепочка для суммаризации документов с помощью GigaChat.

## Установка

Добавьте данные авторизации и настройки GigaChat в переменные окружения, например:
```
    "GIGACHAT_USER": "...",
    "GIGACHAT_PASSWORD": "...",
    "GIGACHAT_VERIFY_SSL_CERTS": "...",
    "GIGACHAT_BASE_URL": "...",
    "GIGACHAT_MODEL": "GigaChat:latest",
```

## Использование

Запустите сервер с помощью команды:
```
    python examples/giga_chain/server.py
```

Запустите пример клиента с помощью команды:
```
    python examples/giga_chain/client.py
```