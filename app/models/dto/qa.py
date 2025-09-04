from app.models.base import PydanticModel


class ChatMessage(PydanticModel):
    role: str
    text: str

    @property
    def to_langchain(self) -> tuple[str, str]:
        return self.role, self.text


class ChatHistory(PydanticModel):
    messages: list[ChatMessage] = []

    def save_asq(self, question: str, response: str) -> None:
        while len(self.messages) > 4:
            self.messages.pop(0)
        self.messages.append(ChatMessage(role="user", text=question))
        self.messages.append(ChatMessage(role="ai", text=response))

    @property
    def to_langchain(self) -> list[tuple[str, str]]:
        return [msg.to_langchain for msg in self.messages]
