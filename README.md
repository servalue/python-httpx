# Python HTTPX Project

## Структура проекта

```
python-httpx/
├── src/                          # Исходный код приложения
│   ├── __init__.py              # Инициализация пакета
│   ├── config.py                # Конфигурация приложения
│   └── models/                  # Модели данных
│       ├── requests/            # Модели запросов
│       │   └── user_requests.py # Пользовательские запросы
│       └── responses/           # Модели ответов
│           └── user_responses.py # Пользовательские ответы
├── tests/                       # Тесты
│   ├── __init__.py             # Инициализация тестового пакета
│   └── api/                    # API тесты
│       ├── __init__.py         # Инициализация API тестов
│       └── test_simple.py      # Простые API тесты
├── conftest.py                 # Конфигурация pytest
├── requirements.txt            # Зависимости проекта
├── libraries.md               # Документация библиотек
├── .gitignore                 # Git игнорируемые файлы
└── README.md                  # Документация проекта
```

### Описание директорий

- **`src/`** - Основной код приложения, организованный по модулям
- **`tests/`** - Все тесты приложения, структура повторяет `src/`
- **`models/`** - Модели данных, разделенные на запросы и ответы
- **`config.py`** - Центральная конфигурация приложения
- **`conftest.py`** - Общие фикстуры и настройки для pytest

## Команды запуска

### Подготовка окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# На macOS/Linux:
source venv/bin/activate
# На Windows:
# venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# API настройки
BASE_URL=https://reqres.in/api
API_KEY=your_api_key_here

# Тестовые данные
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=test_password
```

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск тестов с подробным выводом
pytest -v

# Запуск тестов с генерацией HTML отчета
pytest --html=reports/report.html --self-contained-html

# Запуск тестов с Allure отчетами
pytest --alluredir=allure-results
allure serve allure-results

# Запуск конкретного теста
pytest tests/api/test_simple.py

# Запуск тестов параллельно
pytest -n auto

# Запуск с повторами при падении
pytest --reruns 3
```

### Проверка качества кода

```bash
# Форматирование кода
black src/ tests/

# Линтинг и проверка стиля
ruff check src/ tests/

# Проверка типов
mypy src/
```
