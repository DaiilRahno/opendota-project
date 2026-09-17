# Dota Stats

Учебный проект на Python + FastAPI + JavaScript для получения статистики игрока Dota 2 через OpenDota API.

## Структура

```text
backend/   — бизнес-логика, запросы к OpenDota, схемы и обработка ошибок
routers/   — FastAPI endpoint'ы
frontend/  — HTML/CSS/JavaScript интерфейс
tests/     — pytest unit- и endpoint-тесты
main.py    — точка входа приложения
```

Краткая теория по pytest, mock и схеме FastAPI находится в [`BACKEND_TESTING_GUIDE.md`](BACKEND_TESTING_GUIDE.md).

## Установка

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```bash
python -m pip install -r requirements.txt
```

## Запуск backend

Из корня проекта:

```bash
python -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Frontend

Открыть:

```text
frontend/index.html
```

Frontend обращается к backend по адресу `http://127.0.0.1:8000`.

## Тесты

```bash
python -m pytest
```

Для отображения `print()`:

```bash
python -m pytest -s
```

## Что есть в проекте

- FastAPI endpoint'ы для игрока, винрейта, героев, матчей и summary.
- Pydantic response models и валидация Path/Query параметров.
- Обработка ошибок OpenDota: 404, 502, 504.
- Параллельная загрузка данных `/summary` через `ThreadPoolExecutor`.
- Кэширование справочника героев `/heroes` и `/heroStats` через `lru_cache`.
- Timeout для запросов к OpenDota.
- Unit-тесты, mock-тесты и endpoint-тесты через `TestClient`.
- Frontend на HTML/CSS/JavaScript.

Тестовый Dota account id, который использовался во время разработки: `1008302331`.
