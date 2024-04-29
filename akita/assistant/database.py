from langchain_community.vectorstores import Chroma
from typing import List, Callable


def create_database(texts: List[str], embeddings_provider: Callable) -> Chroma:
    return Chroma.from_documents(documents=texts, embedding=embeddings_provider)
