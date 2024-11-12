from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings


def get_vector_store():
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    return InMemoryVectorStore(embedding)


def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-large")
