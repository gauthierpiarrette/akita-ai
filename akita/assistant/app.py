import chainlit as cl
from akita.assistant.config import SEARCH_TYPE, SEARCH_K
from akita.api.provider_factory import ProviderFactory
from langchain.schema.runnable import RunnableConfig
from akita.assistant.rag_chain import RAGChain


ai_provider = ProviderFactory.get_provider()
rag_chain = RAGChain(ai_provider, SEARCH_TYPE, SEARCH_K)


@cl.on_chat_start
async def on_chat_start() -> None:
    cl.user_session.set("runnable", rag_chain.create_runnable())
    await cl.Message(content="System is ready. You can now ask questions!").send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    runnable = cl.user_session.get("runnable")
    msg = cl.Message(content="")
    async with cl.Step(type="run", name="QA Assistant"):
        async for chunk in runnable.astream(
            message.content,
            config=RunnableConfig(
                callbacks=[
                    cl.LangchainCallbackHandler(),
                    RAGChain.PostMessageHandler(msg),
                ]
            ),
        ):
            await msg.stream_token(chunk)
    await msg.send()
