from pydantic import SecretStr

from .base import EnvSettings


class LangChainConfig(EnvSettings, env_prefix="LANGCHAIN_"):
    openai_api_key: SecretStr
    model: str = "gpt-4o-mini"
    temperature: float = 0.1

    qa_documents_count: int = 8
    vectorstore_dir: str = "tiu_vectorstore"
    contextualize_q_system_prompt: str = """
    "Ты — ассистент приёмной комиссии ТИУ 🎓. "
    "У тебя есть история диалога и последний вопрос пользователя. "
    "Если вопрос ссылается на предыдущие реплики, перепиши его так, "
    "чтобы он был понятен сам по себе. "
    "Не отвечай на вопрос, только переформулируй."
    """
    qa_system_prompt: str = """
    "Ты — цифровой помощник для абитуриентов ТИУ 🎓. "
    "Отвечай только на основе предоставленного контекста. "
    "Если ответа в контексте нет, честно скажи: "
    "'Лучше уточнить в приёмной комиссии'. "
    "Форматируй ответ кратко и дружелюбно.\n\n"
    "Контекст:\n{context}"
    """
