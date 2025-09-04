from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from app.errors.base import AppError

router: Final[Router] = Router(name=__name__)


@router.error(ExceptionTypeFilter(AppError), F.update.message)
async def handle_some_error(error: ErrorEvent) -> Any:
    await error.update.message.answer(text="Что то пошло не так ...")
