from aiogram import Bot, Dispatcher

from app.runners.polling import polling_startup


def run_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher.startup.register(polling_startup)
    return dispatcher.run_polling(bot)
