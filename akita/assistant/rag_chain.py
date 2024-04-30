import chainlit as cl
from typing import List, Dict, Any
from akita.assistant.database import create_database
from akita.assistant.text_splitter import split_texts
from akita.assistant.document_loader import load_documents
from akita.api.base_ai_provider import AIProvider
from langchain.memory import ConversationBufferMemory
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.callbacks.base import BaseCallbackHandler


class RAGChain:
    """
    Class encapsulating the RAG chain setup for processing and answering questions.
    """

    def __init__(self, provider: AIProvider, search_type: str, search_k: int):
        """
        Initializes the RAGChain with necessary
        components for document retrieval and processing.

        Args:
            provider (Any): AI provider capable of providing embeddings
                            and language models.
            search_type (str): Type of search to perform,
                               determines the retrieval strategy.
            search_k (int): Number of top documents to retrieve for processing.
        """
        self.documents: List[Dict[str, Any]] = load_documents()
        self.texts: List[str] = split_texts(self.documents)
        self.embeddings = provider.get_langchain_embeddings()
        self.db = create_database(self.texts, self.embeddings)
        self.retriever = self.db.as_retriever(
            search_type=search_type, search_kwargs={"k": search_k}
        )
        self.llm = provider.get_langchain_provider()
        self.memory = ConversationBufferMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )

    def create_runnable(self) -> RunnablePassthrough:
        """
        Creates a runnable for the chat system to process and
        respond to user queries using retrieved context.

        Returns:
            RunnablePassthrough: Configured runnable chain that
            processes queries based on the retrieved context.
        """
        template = "Answer the question based only on the following context:\
                    \n\n{context}\n\nQuestion: {question}"
        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs: List[Dict[str, Any]]) -> str:
            """
            Formats documents into a single string.

            Args:
                docs (List[Dict[str, Any]]): Documents to format,
                each represented as a dictionary.

            Returns:
                str: Formatted documents.
            """
            return "\n\n".join([doc.page_content for doc in docs])

        return (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    class PostMessageHandler(BaseCallbackHandler):
        """
        Custom callback handler to manage post-retrieval operations
        and append results to the Chainlit message.

        Attributes:
            msg (cl.Message): Chainlit message object to append results.
            sources (Set[Tuple[str, str]]): Set to store unique source and page pairs.
        """

        def __init__(self, msg: cl.Message):
            """
            Initializes the post-message handler with a Chainlit message.

            Args:
                msg (cl.Message): Chainlit message object.
            """
            super().__init__()
            self.msg = msg
            self.sources = set()

        def on_retriever_end(
            self,
            documents: List[Dict[str, Any]],
            *,
            run_id: int,
            parent_run_id: int,
            **kwargs,
        ):
            """
            Handles actions at the end of the retrieval process.

            Args:
                documents (List[Dict[str, Any]]): Retrieved documents.
                run_id (int): Current run identifier.
                parent_run_id (int): Parent run identifier.
            """
            for d in documents:
                source = d.metadata.get("source", "Unknown Source")
                page = d.metadata.get("page", "Unknown Page")
                self.sources.add((source, page))

        def on_llm_end(
            self, response: Dict[str, Any], *, run_id: int, parent_run_id: int, **kwargs
        ):
            """
            Handles actions at the end of the LLM processing.

            Args:
                response (Dict[str, Any]): Response from the LLM.
                run_id (int): Current run identifier.
                parent_run_id (int): Parent run identifier.
            """
            if self.sources:
                sources_text = "\n".join(
                    [f"{source}#page={page}" for source, page in self.sources]
                )
                self.msg.elements.append(
                    cl.Text(name="Sources", content=sources_text, display="inline")
                )
