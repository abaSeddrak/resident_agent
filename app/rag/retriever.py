from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from qdrant_client import models
from app.rag.vector_store import get_vector_store
def retrieve(question:str,app_code:str,language_code:str,k:int=4)->list[Document]:
    tenant_filter= models.Filter(
        must=[
            models.FieldCondition(key="metadata.app_code",match=models.MatchValue(value=app_code)),
            models.FieldCondition(key="metadata.language",match=models.MatchValue(value=language_code))
        ]
    )
    return get_vector_store().similarity_search(question,k,tenant_filter)
