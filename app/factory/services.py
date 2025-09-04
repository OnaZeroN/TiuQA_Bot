from __future__ import annotations

from typing import TypedDict

from app.models.config import AppConfig
from app.services.qa import QAService


class Services(TypedDict):
    qa_service: QAService


def create_services(
    config: AppConfig,
) -> Services:
    qa_service: QAService = QAService(config=config)
    return Services(qa_service=qa_service)
