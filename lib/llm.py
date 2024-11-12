from email import message
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from loguru import logger


async def completion_prompt_list(prompts, vector_store, model="gpt-4o"):
    return [await completion(prompt, vector_store, model) for prompt in prompts]


async def completion(
    prompt,
    vector_store: InMemoryVectorStore,
    model="gpt-4o",
):
    logger.debug("Completing prompt")
    llm = ChatOpenAI(model=model, temperature=0, max_tokens=None, max_retries=3)
    retrieved = vector_store.similarity_search(prompt, k=5)
    messages = [
        (
            "system",
            "You are a helpful assistant. Answer the user's question using the provided context.",
        ),
    ]
    for doc in retrieved:
        messages.append(("user", doc.page_content))
    # append user question
    messages.append(("user", prompt))
    response = await llm.ainvoke(messages)
    logger.debug(f"Completion response: {response.content}")
    return {
        "question": prompt,
        "answer": response.content,
    }
