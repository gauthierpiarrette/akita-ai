from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List


def create_database(texts: List[str]) -> Chroma:
    return Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
