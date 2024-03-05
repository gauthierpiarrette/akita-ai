import chainlit as cl
from akita.assistant.config import MODEL_NAME, SEARCH_TYPE, SEARCH_K
from akita.assistant.database import create_database
from akita.assistant.text_splitter import split_texts
from akita.assistant.document_loader import load_documents
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from typing import List, Dict, Any


documents: List[Dict[str, Any]] = load_documents()
texts: List[str] = split_texts(documents)
db = create_database(texts)
retriever = db.as_retriever(search_type=SEARCH_TYPE, search_kwargs={"k": SEARCH_K})
llm = ChatOpenAI(model_name=MODEL_NAME)
memory = ConversationBufferMemory(
    llm=llm, memory_key="chat_history", return_messages=True, output_key="answer"
)
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory,
    chain_type="stuff",
    return_source_documents=True,
)


@cl.on_chat_start
async def on_chat_start() -> None:
    cl.user_session.set("qa_chain", qa)
    await cl.Message(content="System is ready. You can now ask questions!").send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    qa_chain = cl.user_session.get("qa_chain")
    cb = cl.AsyncLangchainCallbackHandler()
    response = await qa_chain.acall(message.content, callbacks=[cb])
    answer = process_answer(response)
    await cl.Message(content=answer).send()


def process_answer(response: Dict[str, Any]) -> str:
    answer: str = response["answer"]
    source_documents = response.get("source_documents", [])
    if source_documents:
        source_info = [
            doc.metadata.get("source", "Unknown Filename") for doc in source_documents
        ]
        source_info = list(set(source_info))
        # answer += f"\n\nSources: {', '.join(source_info)}"
        # if source_info else "\n\nNo sources found"
    return answer
