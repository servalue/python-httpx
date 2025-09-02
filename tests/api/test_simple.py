import httpx
import pytest
from pydantic import ValidationError
from assertpy import assert_that

from rich import print as rprint
from rich.json import JSON
from src.config import settings
from src.models.responses.user_responses import ListUsersResponse, SingleUserResponse


# Тест на получение списка пользователей
@pytest.mark.asyncio  # Без этого pytest не поймет как запустить async функцию
async def test_get_users():  # тест на получение списка пользователей
    async with httpx.AsyncClient() as client:  # создаем асинхронный клиент
        response = await client.get(
            f"{settings.BASE_URL}/users?page=2&per_page=2", headers=settings.headers
        )  # await - ожидаем ответа от сервера

        rprint(
            "\n📋 [blue]Response url:[/blue]", response.url
        )  # выводим url
        rprint(
            "📋 [blue]Response status code:[/blue]", response.status_code
        )  # выводим статус код

        # проверяем схему через pydantic модель
        try:
            user_response = ListUsersResponse.model_validate(
                response.json()
            )  # проверяем схему
            rprint("✅ [green]Schema validation passed![/green]")
        except ValidationError as e:
            rprint(f"❌ [red]Schema validation failed:[/red] {e}")
            raise

        # проверяем данные с помощью assertpy
        assert_that(response.status_code).described_as(
            "Проверка HTTP статус кода для списка пользователей"
        ).is_equal_to(200)
        assert_that(user_response.page).described_as(
            "Проверка номера страницы в пагинации"
        ).is_equal_to(2)
        assert_that(user_response.per_page).described_as(
            "Проверка количества пользователей на странице"
        ).is_equal_to(2)

        rprint("\n📋 [blue]Response data:[/blue]\n", JSON.from_data(response.json()))   # выводим данные


# ------------------------------------------------------------------------------------------------
# Тест на получение одного пользователя
@pytest.mark.asyncio
async def test_get_single_user():
    async with httpx.AsyncClient() as client:  # создаем асинхронный клиент
        response = await client.get(
            f"{settings.BASE_URL}/users/1", headers=settings.headers
        )

        rprint(
            "\n📋 [blue]Response url:[/blue]", response.url
        )  # выводим url
        rprint(
            "📋 [blue]Response status code:[/blue]", response.status_code
        )  # выводим статус код

        # проверяем схему через pydantic модель
        try:
            user_response = SingleUserResponse.model_validate(
                response.json()
            )  # проверяем схему
            rprint("✅ [green]Schema validation passed![/green]")
        except ValidationError as e:
            rprint(f"❌ [red]Schema validation failed:[/red] {e}")
            raise

        # проверяем данные с помощью assertpy
        assert_that(response.status_code).described_as(
            "Проверка HTTP статус кода для одного пользователя"
        ).is_equal_to(200)
        assert_that(user_response.data.id).described_as(
            "Проверка ID пользователя в ответе API"
        ).is_equal_to(1)
        assert_that(user_response.data.email).described_as(
            "Проверка email адреса пользователя"
        ).is_equal_to("george.bluth@reqres.in")
        assert_that(user_response.data.first_name).described_as(
            "Проверка имени пользователя"
        ).is_equal_to("George")
        assert_that(user_response.data.last_name).described_as(
            "Проверка фамилии пользователя"
        ).is_equal_to("Bluth")
        assert_that(user_response.support.text).described_as(
            "Проверка текста поддержки в ответе"
        ).is_equal_to(
            "Tired of writing endless social media content? Let Content Caddy generate it for you."
        )

        rprint("\n📋 [blue]Response data:[/blue]\n", JSON.from_data(response.json()))   # выводим данные
