# Python Notes For QA Automation

Короткие заметки по Python, которые полезны для API автотестов.

## Функция

Функция - это именованный кусок кода.

```python
def create_user(name, job):
    return {"name": name, "job": job}
```

`name` и `job` - входные данные.

`return` - результат функции.

## Класс

Класс - это шаблон объекта.

```python
class UsersApi:
    def __init__(self, client):
        self.client = client
```

`self` означает "этот конкретный объект".

Через `self.client` мы сохраняем клиент внутри объекта, чтобы потом использовать его в методах.

## Метод

Метод - это функция внутри класса.

```python
def get_user(self, user_id):
    return self.client.get(f"/users/{user_id}")
```

Этот метод делает запрос к пользователю по id.

## assert

`assert` проверяет, что условие истинное.

```python
assert response.status_code == 200
```

Если статус не `200`, тест упадет.

## pytest fixture

Фикстура готовит данные или объект для теста.

```python
@pytest.fixture
def users_api(api_client):
    return UsersApi(api_client)
```

Теперь тест может просто принять `users_api` как аргумент.

pytest сам поймет, что перед тестом нужно вызвать эту фикстуру.

