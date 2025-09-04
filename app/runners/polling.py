from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, loggers

if TYPE_CHECKING:
    from app.models.config import AppConfig


async def polling_startup(bot: Bot, config: AppConfig) -> None:
    await bot.delete_webhook(drop_pending_updates=config.telegram.drop_pending_updates)
    if config.telegram.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")
