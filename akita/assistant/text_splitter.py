from langchain.text_splitter import RecursiveCharacterTextSplitter
from akita.assistant.config import CHUNK_SIZE, CHUNK_OVERLAP
from typing import List, Dict, Any


def split_texts(documents: List[Dict[str, Any]]) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)
