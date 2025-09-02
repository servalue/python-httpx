# Библиотеки для API автотестирования

Подробное описание всех библиотек из requirements.txt для проекта автотестирования API.

## 📡 ОСНОВНЫЕ БИБЛИОТЕКИ ДЛЯ HTTP И ДАННЫХ

### httpx>=0.25.0

**Назначение:** Современный HTTP клиент для Python**Для автотестов:** Отправка API запросов, тестирование REST/GraphQL API, поддержка HTTP/1.1 и HTTP/2**Особенности:**

- Синхронный и асинхронный API
- Автоматическая обработка переадресации
- Поддержка сессий и cookie
- Потоковая загрузка больших файлов
- Настраиваемые таймауты и прокси

**Пример:**

```python
import httpx

# Простой GET запрос
response = httpx.get('https://api.example.com/users')
print(response.json())

# POST с данными
data = {"name": "John", "email": "john@example.com"}
response = httpx.post('https://api.example.com/users', json=data)

# Асинхронный клиент
async def test_api():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/users')
        return response.json()

# Клиент с настройками
with httpx.Client(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer token123"},
    timeout=30.0
) as client:
    response = client.get("/users")
```

### pydantic>=2.5.0

**Назначение:** Валидация данных и создание моделей с использованием типов Python**Для автотестов:** Валидация ответов API, создание тестовых данных, сериализация/десериализация**Особенности:**

- Автоматическая валидация на основе типов
- Генерация JSON Schema
- Поддержка сложных типов данных
- Алиасы полей и настраиваемые валидаторы

**Пример:**

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(ge=0, le=120)
    is_active: bool = True

class UserResponse(BaseModel):
    users: List[User]
    total: int

# Валидация ответа API
def test_api_response():
    response = httpx.get('https://api.example.com/users')
    users_data = UserResponse(**response.json())
    assert users_data.total > 0
    assert all(user.age >= 18 for user in users_data.users if user.age)

# Создание тестовых данных
test_user = User(
    id=1,
    name="Test User",
    email="test@example.com",
    age=25
)
```

### jsonschema>=4.19.0

**Назначение:** Валидация JSON данных по схемам JSON Schema**Для автотестов:** Проверка структуры JSON ответов, валидация API контрактов**Особенности:**

- Поддержка различных версий JSON Schema (Draft 4, 6, 7, 2019-09, 2020-12)
- Детальные сообщения об ошибках
- Настраиваемые форматы и валидаторы

**Пример:**

```python
from jsonschema import validate, ValidationError, Draft202012Validator

# Схема для пользователя
user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer", "minimum": 0, "maximum": 120}
    },
    "required": ["id", "name", "email"]
}

def test_user_schema():
    response = httpx.get('https://api.example.com/users/1')
    user_data = response.json()
  
    try:
        validate(instance=user_data, schema=user_schema)
        print("Валидация прошла успешно")
    except ValidationError as e:
        print(f"Ошибка валидации: {e.message}")
        print(f"Путь к ошибке: {e.absolute_path}")

# Создание валидатора
validator = Draft202012Validator(user_schema)
errors = list(validator.iter_errors(user_data))
for error in errors:
    print(f"Ошибка в поле {error.json_path}: {error.message}")
```

## 🧪 ФРЕЙМВОРК ДЛЯ ТЕСТИРОВАНИЯ

### pytest>=7.4.0

**Назначение:** Основной фреймворк для написания и запуска тестов**Для автотестов:** Создание тестовых сценариев, группировка тестов, генерация отчетов**Особенности:**

- Простой синтаксис assert
- Фикстуры для подготовки данных
- Параметризация тестов
- Плагины и расширения

**Пример:**

```python
import pytest
import httpx

# Базовые тесты
def test_api_status():
    response = httpx.get('https://api.example.com/health')
    assert response.status_code == 200

def test_user_creation():
    user_data = {"name": "John", "email": "john@example.com"}
    response = httpx.post('https://api.example.com/users', json=user_data)
    assert response.status_code == 201
    assert response.json()["name"] == "John"

# Параметризованные тесты
@pytest.mark.parametrize("user_id,expected_name", [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie")
])
def test_get_user(user_id, expected_name):
    response = httpx.get(f'https://api.example.com/users/{user_id}')
    assert response.status_code == 200
    assert response.json()["name"] == expected_name

# Фикстуры
@pytest.fixture
def api_client():
    return httpx.Client(base_url="https://api.example.com")

@pytest.fixture
def test_user():
    return {"name": "Test User", "email": "test@example.com"}

def test_with_fixtures(api_client, test_user):
    response = api_client.post("/users", json=test_user)
    assert response.status_code == 201
```

### pytest-asyncio>=0.21.0

**Назначение:** Поддержка асинхронных тестов в pytest**Для автотестов:** Тестирование асинхронного кода, параллельная обработка запросов**Особенности:**

- Декораторы для async/await тестов
- Управление циклами событий
- Асинхронные фикстуры

**Пример:**

```python
import pytest
import asyncio
import httpx

@pytest.mark.asyncio
async def test_async_api_call():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/users')
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_multiple_requests():
    async with httpx.AsyncClient() as client:
        # Параллельные запросы
        tasks = [
            client.get(f'https://api.example.com/users/{i}')
            for i in range(1, 6)
        ]
        responses = await asyncio.gather(*tasks)
        assert all(r.status_code == 200 for r in responses)

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        yield client

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
```

### pytest-xdist>=3.3.0

**Назначение:** Параллельное выполнение тестов**Для автотестов:** Ускорение выполнения больших наборов тестов**Особенности:**

- Запуск тестов на нескольких CPU
- Распределение по удаленным машинам
- Автоматическое балансирование нагрузки

**Пример использования:**

```bash
# Запуск на всех доступных CPU
pytest -n auto

# Запуск на 4 процессах
pytest -n 4

# Распределение по логической группировке
pytest --dist loadgroup
```

## 📊 ОТЧЕТНОСТЬ И ЛОГИРОВАНИЕ

### allure-pytest>=2.13.0

**Назначение:** Генерация красивых и подробных отчетов о тестировании**Для автотестов:** Создание интерактивных отчетов с деталями выполнения тестов**Особенности:**

- Веб-интерфейс для просмотра результатов
- Группировка тестов по функциональности
- Вложения (логи, скриншоты, данные)
- История выполнения тестов

**Пример:**

```python
import allure
import httpx

@allure.feature("User Management")
@allure.story("User Creation")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    with allure.step("Подготовка данных пользователя"):
        user_data = {"name": "John", "email": "john@example.com"}
      
    with allure.step("Отправка запроса на создание"):
        response = httpx.post('https://api.example.com/users', json=user_data)
      
    with allure.step("Проверка ответа"):
        assert response.status_code == 201
        user = response.json()
        assert user["name"] == "John"
      
    allure.attach(str(user), "Created User", allure.attachment_type.JSON)

@allure.feature("User Management")
@allure.story("User Retrieval")
def test_get_user():
    user_id = 1
    with allure.step(f"Получение пользователя с ID {user_id}"):
        response = httpx.get(f'https://api.example.com/users/{user_id}')
      
    assert response.status_code == 200
    allure.attach(response.text, "API Response", allure.attachment_type.JSON)
```

### pytest-html>=4.1.0

**Назначение:** Генерация HTML отчетов для pytest**Для автотестов:** Создание простых HTML отчетов о результатах тестирования**Особенности:**

- Встроенные CSS стили
- Группировка по результатам
- Детали ошибок и трассировки

**Пример использования:**

```bash
# Генерация HTML отчета
pytest --html=report.html --self-contained-html

# С дополнительными деталями
pytest --html=report.html --capture=no
```

## 🔧 ДОПОЛНИТЕЛЬНЫЕ ИНСТРУМЕНТЫ ДЛЯ АВТОТЕСТОВ

### python-dotenv>=1.0.0

**Назначение:** Работа с переменными окружения из .env файлов**Для автотестов:** Управление конфигурацией тестов для разных окружений**Особенности:**

- Загрузка переменных из файлов
- Поддержка множественных .env файлов
- Приоритет переменных

**Пример:**

```python
from dotenv import load_dotenv
import os
import httpx

# Загрузка переменных окружения
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
API_TOKEN = os.getenv("API_TOKEN")

@pytest.fixture
def authenticated_client():
    headers = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}
    return httpx.Client(base_url=API_BASE_URL, headers=headers)

def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get("/protected")
    assert response.status_code == 200
```

**.env файл:**

```
API_BASE_URL=https://staging-api.example.com
API_TOKEN=your_test_token_here
DATABASE_URL=postgresql://test:test@localhost/testdb
DEBUG=True
```

### pytest-rerunfailures>=12.0

**Назначение:** Повторный запуск упавших тестов**Для автотестов:** Обработка нестабильных тестов, зависящих от внешних сервисов**Особенности:**

- Настраиваемое количество повторов
- Задержка между попытками
- Фильтрация по типу ошибок

**Пример использования:**

```bash
# Повтор упавших тестов до 3 раз
pytest --reruns 3

# С задержкой между попытками
pytest --reruns 3 --reruns-delay 1

# Только для определенных исключений
pytest --reruns 3 --only-rerun "ConnectionError"
```

**В коде:**

```python
import pytest

@pytest.mark.flaky(reruns=5, reruns_delay=2)
def test_unstable_api():
    response = httpx.get('https://unstable-api.example.com/data')
    assert response.status_code == 200
```

## 🛠️ КАЧЕСТВО КОДА И ТИПИЗАЦИЯ

### ruff>=0.1.0

**Назначение:** Сверхбыстрый линтер и форматтер для Python**Для автотестов:** Проверка качества кода тестов, соблюдение стандартов**Особенности:**

- Замена flake8, isort, black в одном инструменте
- Автоматическое исправление ошибок
- Настраиваемые правила

**Конфигурация (pyproject.toml):**

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.ruff.per-file-ignores]
"tests/*" = ["F401", "F811"]  # Разрешить неиспользуемые импорты в тестах
```

### black>=23.0.0

**Назначение:** Автоматический форматтер кода Python**Для автотестов:** Единообразное форматирование кода тестов**Особенности:**

- Неизменяемый стиль форматирования
- Быстрая работа
- Интеграция с редакторами

**Конфигурация:**

```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### mypy>=1.7.0

**Назначение:** Статическая проверка типов Python**Для автотестов:** Обнаружение ошибок типизации в тестовом коде**Особенности:**

- Постепенная типизация
- Поддержка type hints
- Интеграция с IDE

**Пример типизированного теста:**

```python
from typing import Dict, List, Optional
import httpx

def get_user_by_id(user_id: int) -> Optional[Dict[str, any]]:
    response: httpx.Response = httpx.get(f'https://api.example.com/users/{user_id}')
    if response.status_code == 200:
        return response.json()
    return None

def test_typed_api_call() -> None:
    user: Optional[Dict[str, any]] = get_user_by_id(1)
    assert user is not None
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
```

### typing-extensions>=4.8.0

**Назначение:** Расширения для системы типов Python**Для автотестов:** Использование новых возможностей типизации в старых версиях Python**Особенности:**

- Обратная совместимость новых типов
- Protocol, Literal, TypedDict
- Аннотации для runtime

**Пример:**

```python
from typing_extensions import Protocol, Literal, TypedDict

class APIClient(Protocol):
    def get(self, url: str) -> httpx.Response: ...
    def post(self, url: str, json: dict) -> httpx.Response: ...

class UserDict(TypedDict):
    id: int
    name: str
    status: Literal["active", "inactive", "pending"]

def test_with_protocols(client: APIClient) -> None:
    response = client.get("/users/1")
    user: UserDict = response.json()
    assert user["status"] in ("active", "inactive", "pending")
```

Этот документ предоставляет полное понимание каждой библиотеки, её роли в автотестировании API и практические примеры использования.
