from __future__ import annotations

from app.models.config.env import (
    AppConfig,
    CommonConfig,
    TelegramConfig,
    LangChainConfig,
)


# noinspection PyArgumentList
def create_app_config() -> AppConfig:
    return AppConfig(
        common=CommonConfig(),
        telegram=TelegramConfig(),
        langchain=LangChainConfig(),
    )
