# Dota Analytics

Backend-приложение для получения и анализа статистики игроков Dota 2 на основе OpenDota API.

Проект создан в учебных целях для практики backend-разработки на Python. В нём используются FastAPI, Pydantic, работа с внешним API, обработка ошибок, параллельная загрузка данных, локальное кэширование, тестирование, frontend и Docker.

---

## Возможности

Приложение умеет:

- получать информацию о профиле игрока;
- рассчитывать общий winrate;
- получать статистику по героям;
- получать последние рейтинговые матчи;
- рассчитывать KDA;
- рассчитывать средний KDA;
- определять лучший и худший матч;
- формировать агрегированную статистику через `/summary`;
- обрабатывать ошибки OpenDota API;
- обрабатывать timeout и проблемы соединения;
- кэшировать готовый результат `/summary`;
- кэшировать справочники героев;
- отображать статистику через frontend.

---

## Технологии

### Backend

- Python
- FastAPI
- Pydantic
- Requests
- ThreadPoolExecutor
- Pytest
- FastAPI TestClient

### Frontend

- HTML
- CSS
- JavaScript

### Инфраструктура и инструменты

- Docker
- Git
- OpenDota API

---

## Структура проекта

```text
project/
├── backend/
│   ├── __init__.py
│   ├── api.py
│   ├── app.py
│   ├── cache.py
│   ├── errors.py
│   ├── heroes.py
│   ├── matches.py
│   ├── player.py
│   ├── schemas.py
│   ├── stats.py
│   └── winrate.py
│
├── routers/
│   ├── __init__.py
│   ├── heroes.py
│   ├── matches.py
│   ├── player.py
│   ├── summary.py
│   └── winrate.py
│
├── frontend/
├── tests/
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### Назначение директорий

- `backend/` — бизнес-логика приложения.
- `routers/` — FastAPI endpoints.
- `tests/` — unit-, mock-, endpoint- и cache-тесты.
- `frontend/` — пользовательский интерфейс.
- `main.py` — точка входа в приложение.
- `Dockerfile` — инструкция для сборки Docker image.

---

## API endpoints

### Player

```http
GET /player/{account_id}
```

Возвращает основную информацию об игроке.

Пример:

```text
/player/1008302331
```

---

### Winrate

```http
GET /winrate/{account_id}
```

Возвращает:

- количество побед;
- количество поражений;
- количество игр;
- winrate.

---

### Heroes

```http
GET /heroes/{account_id}
```

Возвращает статистику по героям игрока.

В статистику попадают герои, удовлетворяющие условиям бизнес-логики приложения.

---

### Matches

```http
GET /matches/{account_id}
```

Возвращает последние рейтинговые матчи игрока.

---

### Summary

```http
GET /summary/{account_id}
```

Главный агрегирующий endpoint приложения.

Он объединяет:

- данные игрока;
- общий winrate;
- статистику по героям;
- последние матчи;
- средний KDA;
- лучший матч;
- худший матч.

Количество матчей можно передать через query parameter:

```text
/summary/1008302331?count=20
```

Допустимый диапазон:

```text
1 <= count <= 100
```

По умолчанию:

```text
count=7
```

---

## Параллельная загрузка данных

Для уменьшения времени ответа `/summary` используется `ThreadPoolExecutor`.

Вместо последовательной загрузки:

```text
player
↓
winrate
↓
heroes
↓
matches
```

запросы выполняются параллельно:

```text
player    ─┐
winrate   ─┤
heroes    ─┼─→ summary
matches   ─┘
```

В результате общее время ожидания в основном зависит от самого медленного внешнего запроса.

---

## Кэширование

Для `/summary` реализован локальный TTL-кэш.

Кэш хранится в оперативной памяти Python-приложения.

Ключ кэша:

```python
(account_id, count)
```

Пример:

```python
(1008302331, 20)
```

Это позволяет отдельно хранить результаты одного игрока для разного количества матчей.

Значение кэша:

```python
(expires_at, data)
```

где:

- `expires_at` — момент, после которого запись считается устаревшей;
- `data` — готовый результат `/summary`.

Логика:

```text
Запрос /summary
        ↓
Проверка кэша
        ↓
   данные есть?
    /       \
  да         нет
  ↓           ↓
return     OpenDota API
              ↓
         собрать summary
              ↓
         сохранить в кэш
              ↓
            return
```

Если TTL истёк, старая запись удаляется, после чего данные загружаются заново.

Для измерения времени жизни записи используется:

```python
time.monotonic()
```

### Кэширование справочников героев

Справочники героев меняются редко, поэтому для них используется `lru_cache`.

Это уменьшает количество одинаковых запросов к OpenDota API.

---

## Обработка ошибок

Приложение обрабатывает основные ошибки при работе с OpenDota API.

Используются следующие HTTP-коды:

```text
404 — игрок не найден
502 — ошибка OpenDota API или проблема соединения
504 — OpenDota API не ответил вовремя
422 — ошибка валидации входных параметров FastAPI
```

Например:

```text
/player/0
```

не проходит валидацию, так как `account_id` должен быть больше либо равен `1`.

---

## Валидация данных

Для валидации входных и выходных данных используются:

- FastAPI `Path`;
- FastAPI `Query`;
- Pydantic `BaseModel`;
- Pydantic `Field`.

Пример параметра:

```python
account_id: int = Path(ge=1)
```

Пример query parameter:

```python
count: int = Query(7, ge=1, le=100)
```

---

## Тестирование

В проекте используются:

- unit-тесты;
- mock-тесты;
- endpoint-тесты;
- тесты обработки ошибок;
- тесты кэширования.

Mock используется для изоляции собственной бизнес-логики от внешнего OpenDota API.

Для endpoint-тестов используется FastAPI `TestClient`.

Он позволяет тестировать API без запуска реального Uvicorn-сервера.

### Запуск всех тестов

```bash
python -m pytest
```

Текущий результат:

```text
29 passed
```

Предупреждения сторонних библиотек могут отображаться отдельно и не влияют на успешность прохождения тестов.

---

## Локальный запуск

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
```

Перейти в папку проекта:

```bash
cd <project-folder>
```

---

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows cmd

```cmd
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

### 3. Установить зависимости

```bash
python -m pip install -r requirements.txt
```

---

### 4. Запустить backend

```bash
python -m uvicorn main:app --reload
```

После запуска API доступно по адресу:

```text
http://127.0.0.1:8000
```

---

## Swagger и документация API

FastAPI автоматически генерирует интерактивную документацию.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Через Swagger можно:

- посмотреть все endpoints;
- увидеть параметры запросов;
- посмотреть схемы ответов;
- отправить тестовый запрос прямо из браузера.

---

## Frontend

Frontend написан на:

- HTML;
- CSS;
- JavaScript.

Он отправляет запрос к:

```text
/summary/{account_id}
```

и отображает:

- nickname;
- Steam ID;
- winrate;
- лучших героев;
- последние матчи;
- средний KDA;
- лучший матч;
- худший матч.

Frontend также поддерживает выбор количества загружаемых матчей.

---

## Docker

В проект добавлены:

```text
Dockerfile
.dockerignore
```

### Сборка Docker image

```bash
docker build -t dota-api .
```

### Запуск контейнера

```bash
docker run --name dota-api-container -p 8000:8000 dota-api
```

После запуска API должно быть доступно по адресу:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Остановка контейнера

```bash
docker stop dota-api-container
```

### Повторный запуск

```bash
docker start dota-api-container
```

### Удаление контейнера

```bash
docker rm dota-api-container
```

### Просмотр локальных images

```bash
docker images
```

### Просмотр контейнеров

```bash
docker ps -a
```

> Dockerfile уже добавлен в проект. Финальную проверку сборки и запуска контейнера необходимо выполнить на машине с доступной аппаратной виртуализацией и работающим Docker Engine.

---

## Dockerfile

Используется облегчённый Python image:

```dockerfile
FROM python:3.12-slim
```

Приложение внутри контейнера запускается через Uvicorn:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Параметр:

```text
--host 0.0.0.0
```

нужен для того, чтобы приложение было доступно извне контейнера.

---

## Тестовый Dota account id

Во время разработки использовался:

```text
1008302331
```

Пример запроса:

```text
http://127.0.0.1:8000/summary/1008302331?count=20
```

---

## Основные изученные темы

В процессе разработки были практически отработаны:

- FastAPI;
- REST API;
- работа с внешним API;
- HTTP requests;
- Pydantic;
- валидация;
- обработка исключений;
- timeout;
- ThreadPoolExecutor;
- in-memory cache;
- TTL cache;
- lru_cache;
- pytest;
- mock;
- TestClient;
- Docker;
- HTML;
- CSS;
- JavaScript;
- Git.

---

## Ограничения текущей версии

Текущая версия использует локальный in-memory cache.

Это означает:

- кэш очищается при перезапуске приложения;
- разные процессы приложения не разделяют общий кэш;
- кэш не предназначен для нескольких backend-инстансов;
- приложение пока не хранит историю запросов в базе данных;
- нет авторизации пользователей;
- нет централизованного логирования;
- Docker-сборка пока требует финальной проверки на машине с доступной виртуализацией.

---

## Дальнейшее развитие проекта

### Кэширование

Вместо локального словаря можно использовать Redis.

Это позволит:

- использовать общий кэш между несколькими экземплярами приложения;
- сохранять кэш независимо от процесса Python;
- масштабировать backend.

### База данных

Добавить PostgreSQL для хранения:

- пользователей;
- сохранённых Dota-профилей;
- истории запросов;
- избранных игроков;
- пользовательских настроек.

Планируемый стек:

```text
PostgreSQL
SQLAlchemy
Alembic
```

### Авторизация

Добавить:

- регистрацию;
- вход;
- JWT access token;
- refresh token;
- защищённые endpoints.

### Конфигурация

Перенести настройки приложения в environment variables.

Например:

```text
OPEN_DOTA_API_URL
CACHE_TTL_SECONDS
REQUEST_TIMEOUT
```

Использовать `.env` файл только для локальной разработки.

### Логирование

Добавить структурированное логирование:

- внешних запросов;
- timeout;
- ошибок;
- cache hit;
- cache miss;
- времени выполнения `/summary`.

### CI/CD

Добавить pipeline, который при каждом push или merge request:

```text
install dependencies
        ↓
run tests
        ↓
build Docker image
        ↓
deploy
```

Возможные инструменты:

- GitHub Actions;
- GitLab CI/CD.

### Production deployment

В дальнейшем приложение можно развернуть на сервере или облачной платформе.

Возможная схема:

```text
Internet
   ↓
Nginx
   ↓
FastAPI / Uvicorn
   ↓
Redis
   ↓
PostgreSQL
   ↓
OpenDota API
```

### Frontend

Возможные улучшения:

- адаптивная мобильная версия;
- графики winrate и KDA;
- история матчей;
- фильтрация по героям;
- сравнение игроков;
- сохранение избранных профилей;
- отдельная страница матча.

### Мониторинг

Для production-версии можно добавить:

- health-check endpoint;
- Prometheus metrics;
- Grafana;
- централизованный сбор логов.

---

## Возможная архитектура будущей версии

```text
Frontend
   ↓
FastAPI
   ├── PostgreSQL
   ├── Redis
   └── OpenDota API
```

В production:

```text
Client
  ↓
Nginx
  ↓
FastAPI
  ├── Redis
  ├── PostgreSQL
  └── OpenDota API
```

---

## Статус проекта

На текущем этапе реализованы:

- основные API endpoints;
- Pydantic-схемы;
- валидация;
- обработка ошибок;
- timeout внешних запросов;
- параллельная загрузка данных;
- локальное кэширование;
- кэширование справочников;
- frontend;
- unit-тесты;
- mock-тесты;
- endpoint-тесты;
- cache-тесты;
- Dockerfile;
- `.dockerignore`.

Следующий этап:

1. проверить Docker build и запуск контейнера;
2. привести GitHub-репозиторий к финальному виду;
3. добавить CI/CD;
4. при необходимости развивать проект с PostgreSQL, Redis и авторизацией.
