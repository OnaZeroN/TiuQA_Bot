from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import TelegramObject
from aiogram import html
from aiogram.utils.link import create_tg_link


if TYPE_CHECKING:
    from app.services.qa import QAService
    from app.telegram.helpers import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def greeting(
    _: TelegramObject,
    helper: MessageHelper,
) -> Any:
    user = helper.update.chat
    mention = html.link(value=user.first_name, link=create_tg_link("user", id=user.id))

    return await helper.answer(
        text=(
            f"Привет, {mention}! 👋 Я твой цифровой помощник по поступлению в ТИУ."
            "Я могу быстро ответить на самые популярные вопросы о поступлении или помочь найти нужный раздел на сайте."
        )
    )


@router.message(flags={"long_operation": "typing"})
async def answer(
    _: TelegramObject, helper: MessageHelper, qa_service: QAService
) -> Any:
    msg = await helper.answer(text="Ищу ответ ...", reply=True)
    await helper.answer(
        message_id=msg.message_id,
        text=await qa_service.asq(
            context=helper.fsm,
            question=helper.update.text,
        ),
        force_edit=True,
    )
