import json
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

OPENAI_API_KEY = os.environ.get("LANGCHAIN_OPENAI_API_KEY")

with open("assets/tiu_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

docs = []
for item in data:
    category = item.get("category", "Общее")
    content = item.get("content", "")
    qa = item.get("qa", [])

    if qa:
        for pair in qa:
            text = f"Вопрос: {pair['q']}\nОтвет: {pair['a']}"
            docs.append(
                Document(
                    page_content=text, metadata={"category": category, "id": item["id"]}
                )
            )
    else:
        text = (
            json.dumps(content, ensure_ascii=False, indent=2)
            if isinstance(content, dict)
            else str(content)
        )
        docs.append(
            Document(
                page_content=text, metadata={"category": category, "id": item["id"]}
            )
        )

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
splitted_docs = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
vectorstore = Chroma.from_documents(
    splitted_docs, embedding=embeddings, persist_directory="tiu_vectorstore"
)
