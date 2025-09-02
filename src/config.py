"""Настройки приложения."""

import os
from typing import Dict
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class Settings:
    """Простые настройки для автотестов ReqRes API."""
    
    # API Configuration
    BASE_URL: str = os.getenv("BASE_URL")
    API_KEY: str = os.getenv("API_KEY")  
    
    # Test Configuration  
    TEST_USER_EMAIL: str = os.getenv("TEST_USER_EMAIL")
    TEST_USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD")
    
    @property                                       # Делает метод "как переменную"
    def headers(self) -> Dict[str, str]:
        """HTTP заголовки для запросов к API."""
        return {
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/json'
        }


# Глобальный экземпляр настроек
settings = Settings()
