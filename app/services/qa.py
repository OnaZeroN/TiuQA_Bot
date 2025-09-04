from aiogram.fsm.context import FSMContext

from langchain_chroma import Chroma
from langchain_core.runnables import Runnable
from langchain_core.vectorstores import VectorStoreRetriever

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

from app.errors.base import AppError
from app.models.config import AppConfig
from app.models.dto.qa import ChatHistory

from .base import BaseService


class QAService(BaseService):
    config: AppConfig

    llm: ChatOpenAI
    vectorstore: Chroma
    retriever: VectorStoreRetriever

    chain: Runnable

    def __init__(self, config: AppConfig):
        super().__init__()

        self.config = config

        self.llm = ChatOpenAI(
            model=self.config.langchain.model,
            temperature=self.config.langchain.temperature,
            api_key=self.config.langchain.openai_api_key,
        )
        self.vectorstore = Chroma(
            persist_directory=self.config.langchain.vectorstore_dir,
            embedding_function=OpenAIEmbeddings(
                api_key=self.config.langchain.openai_api_key
            ),
        )
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.config.langchain.qa_documents_count}
        )
        self.chain = self.__build_chain()

    async def asq(self, context: FSMContext, question: str) -> str:
        try:
            self.logger.info(
                f"New asq | User {context.key.user_id} | Question - {question}"
            )
            chat_history = ChatHistory.model_validate(await context.get_data())
            response = await self.chain.ainvoke(
                {"input": question, "chat_history": chat_history.to_langchain}
            )
            chat_history.save_asq(question=question, response=response["answer"])
            await context.update_data(chat_history.model_dump())
            self.logger.info(
                f"New response | User {context.key.user_id} | Response - {response['answer']}"
            )
            return response["answer"]
        except Exception as e:
            self.logger.error(
                f"Failed asq | User {context.key.user_id} | Question - {question} | Error - {e}"
            )
            raise AppError(e)

    def __build_chain(self):
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.config.langchain.contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.config.langchain.qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)

        return create_retrieval_chain(history_aware_retriever, question_answer_chain)
