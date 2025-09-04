from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from app.factory.services import create_services
from app.models.config import AppConfig, Assets
from app.telegram.handlers import extra, main
from app.telegram.middlewares import MessageHelperMiddleware, ChatActionMiddleware


def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    # noinspection PyArgumentList
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=MemoryStorage(),
        config=config,
        assets=Assets(),
        **create_services(
            config=config,
        ),
    )

    dispatcher.include_routers(main.router, extra.router)
    dispatcher.update.outer_middleware(MessageHelperMiddleware())
    dispatcher.message.middleware(ChatActionMiddleware())
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    return dispatcher
