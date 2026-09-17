# Шпаргалка: pytest, mock и FastAPI

Этот файл — короткая теория именно по тому, что используется в проекте Dota Stats.

## 1. Что делает обычный тест

Самая простая схема теста:

```text
Подготовка данных -> вызов функции -> проверка результата
Arrange          -> Act          -> Assert
```

Пример:

```python
def test_calculate_kda():
    result = calculate_kda(10, 5, 10)
    assert result == 4.0
```

`assert` означает: "я ожидаю, что выражение справа/условие будет истинным".
Если условие ложно, pytest помечает тест как упавший.

Запуск всех тестов:

```bash
python -m pytest
```

Показать `print()` во время тестов:

```bash
python -m pytest -s
```

Более подробный вывод:

```bash
python -m pytest -vv
```

Запустить один файл:

```bash
python -m pytest tests/test_endpoint.py
```

Запустить один тест:

```bash
python -m pytest tests/test_endpoint.py::test_player_timeout -vv
```

## 2. Зачем нужен mock

Mock — временная подмена зависимости во время теста.

Мы не хотим в unit-тесте реально обращаться к OpenDota, потому что внешний API может:

- медленно отвечать;
- быть недоступен;
- вернуть 404/500;
- зависеть от интернета;
- изменить данные.

Поэтому внешний мир подменяем, а наш код оставляем настоящим.

```text
Без mock:
наш код -> requests -> интернет -> OpenDota

С mock:
наш код -> mock -> заранее заданный результат
```

Главная идея:

> Mock позволяет создать контролируемую ситуацию и проверить реакцию нашего кода.

## 3. `patch()`

Пример из проекта:

```python
with patch("backend.player.make_request") as mock_request:
    ...
```

На время блока `with` настоящий `make_request` заменяется объектом mock.
После выхода из `with` всё возвращается обратно.

### Где делать patch

Патчим имя **там, где тестируемый код его использует**.

Например, `backend/player.py` содержит:

```python
from backend.api import make_request
```

Поэтому для теста `get_player()`:

```python
patch("backend.player.make_request")
```

А endpoint `routers/player.py` использует:

```python
from backend.player import get_player
```

Поэтому endpoint-тест патчит:

```python
patch("routers.player.get_player")
```

Запомнить можно так:

> Patch where it is looked up — подменяй там, где функция ищется во время выполнения.

## 4. `return_value`

`return_value` задаёт то, что mock-функция вернёт.

```python
with patch("backend.player.make_request") as mock_request:
    mock_request.return_value = {"hello": "world"}

    result = get_player(123)

    assert result == {"hello": "world"}
```

Мысленно это означает:

```text
"Представим, что API вернул вот эти данные"
```

Важно:

```python
mock.return_value = value
```

а не:

```python
mock.return_value.value = value
```

## 5. `side_effect`

`side_effect` удобно использовать, когда зависимость должна не вернуть результат, а выбросить исключение.

```python
mock_get_player.side_effect = Timeout()
```

Мысленно:

```text
"Представим, что OpenDota не ответил вовремя"
```

Тогда можно проверить реакцию нашего backend:

```python
response = client.get("/player/123")
assert response.status_code == 504
```

Примеры из проекта:

```text
HTTPError с 404 -> наш API возвращает 404
ConnectionError -> наш API возвращает 502
Timeout         -> наш API возвращает 504
```

Коротко:

```text
return_value = зависимость успешно вернула данные
side_effect  = зависимость выбросила ошибку
```

## 6. Проверка вызова mock

Mock запоминает, как его вызывали.

```python
mock_request.assert_called_once_with(
    "https://api.opendota.com/api/players/123"
)
```

Это проверяет одновременно:

- функция была вызвана;
- ровно один раз;
- с указанными аргументами.

Дополнительный `assert` писать не нужно:

```python
# правильно
mock_request.assert_called_once_with(123)

# неправильно
assert mock_request.assert_called_once_with(123)
```

Почему второй вариант плох: `assert_called_once_with()` уже сам делает проверку и при успехе возвращает `None`.

Посмотреть фактические аргументы вызова:

```python
print(mock_request.call_args)
```

## 7. Что такое endpoint-тест

Unit-тест обычно вызывает Python-функцию напрямую:

```python
result = prepare_player(data)
```

Endpoint-тест имитирует HTTP-запрос к FastAPI:

```python
response = client.get("/player/123")
```

Для этого используется:

```python
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)
```

`TestClient` не отправляет настоящий сетевой запрос на `localhost:8000`.
Он прогоняет запрос через FastAPI внутри процесса тестов.

Концептуально:

```text
client.get("/player/123")
        |
        v
FastAPI router
        |
        v
наша backend-логика
        |
        v
HTTP response
```

По смыслу это похоже на:

```text
GET http://127.0.0.1:8000/player/123
```

но отдельно запускать Uvicorn для теста не нужно.

## 8. Объект `response`

```python
response = client.get("/player/123")
```

`response` — объект ответа. Часто используем:

```python
response.status_code
response.json()
response.text
response.headers
```

Например:

```python
assert response.status_code == 200
assert response.json()["nickname"] == "TestPlayer"
```

Не нужно ничего отдельно импортировать для `.status_code` — это свойство объекта response.

Правильно:

```python
response.status_code
```

Неправильно:

```python
response.status.code
```

## 9. Почему FastAPI возвращает 422

Например роутер содержит:

```python
account_id: int = Path(ge=1)
```

Если вызвать:

```text
/player/0
```

FastAPI остановит запрос ещё до нашей бизнес-логики и вернёт `422`, потому что `0` не удовлетворяет `ge=1`.

Аналогично:

```python
count: int = Query(7, ge=1, le=100)
```

даёт `422` для `count=0` или `count>100`.

## 10. Как FastAPI работает в этом проекте

Упрощённая схема обычного запроса:

```text
Frontend (script.js)
        |
        | GET /summary/{account_id}?count=...
        v
FastAPI app (backend/app.py)
        |
        v
Router (routers/summary.py)
        |
        +-------------------------------+
        |                               |
        v                               v
backend/player.py                 backend/winrate.py
backend/heroes.py                 backend/matches.py
        |                               |
        +---------------+---------------+
                        |
                        v
                 backend/api.py
                        |
                        | requests.get(...)
                        v
                   OpenDota API
                        |
                        v
                 JSON-данные назад
                        |
                        v
             подготовка/расчёты данных
                        |
                        v
              Pydantic response_model
                        |
                        v
                  JSON response
                        |
                        v
                     Frontend
```

В `/summary` четыре независимых получения данных запускаются через `ThreadPoolExecutor`, поэтому они могут ждать OpenDota параллельно, а не строго друг за другом.

## 11. Роль файлов проекта

```text
main.py
  точка входа для Uvicorn

backend/app.py
  создаёт FastAPI и подключает routers

routers/*.py
  описывают URL, Path/Query параметры и HTTP response_model

backend/*.py
  бизнес-логика и работа с OpenDota

backend/schemas.py
  Pydantic-схемы ответов

backend/errors.py
  перевод ошибок requests в 404/502/504

tests/*.py
  unit- и endpoint-тесты
```

## 12. Быстрая памятка

```text
assert                       -> проверить значение/условие
patch(...)                   -> временно подменить зависимость
mock.return_value            -> задать успешный результат mock
mock.side_effect             -> заставить mock выбросить ошибку
mock.assert_called_once_with -> проверить вызов и аргументы
mock.call_args               -> посмотреть реальные аргументы вызова
TestClient                   -> имитация HTTP-запросов к FastAPI
response.status_code         -> HTTP-код ответа
response.json()              -> JSON ответа как Python dict/list
```

## 13. Команды проекта

Установить зависимости:

```bash
python -m pip install -r requirements.txt
```

Запустить backend из корня проекта:

```bash
python -m uvicorn main:app --reload
```

Запустить тесты:

```bash
python -m pytest
```

Запустить тесты с `print()`:

```bash
python -m pytest -s
```

API после запуска:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```
