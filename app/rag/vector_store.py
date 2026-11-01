from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.config import settings

COLLECTION_NAME = "compound_content"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)


def get_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
        url=settings.qdrant_url,
    )