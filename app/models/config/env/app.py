from pydantic import BaseModel

from .common import CommonConfig
from .telegram import TelegramConfig
from .langchain import LangChainConfig


class AppConfig(BaseModel):
    telegram: TelegramConfig
    common: CommonConfig
    langchain: LangChainConfig
