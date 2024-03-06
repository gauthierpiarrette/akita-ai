from akita.assistant.config import GLOB_PATTERN, SUFFIXES, EXCLUDE_PATTERNS, ENV
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.document_loaders.generic import GenericLoader
import os
from typing import List, Dict, Any


def load_documents() -> List[Dict[str, Any]]:
    repo_path: str = ENV.get("REPO_PATH", os.getcwd())
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob=GLOB_PATTERN,
        suffixes=SUFFIXES,
        exclude=EXCLUDE_PATTERNS,
        parser=LanguageParser(),
    )
    documents = loader.load()

    if not documents:
        raise ValueError(
            f"No file found within the specified repository path: {repo_path}"
        )

    return documents
