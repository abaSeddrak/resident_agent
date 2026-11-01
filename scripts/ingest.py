from langchain_qdrant import QdrantVectorStore

from app.clients.cityeye_client import get_compound_content
from app.config import settings
from app.rag.chunking import build_documents
from app.rag.vector_store import COLLECTION_NAME, embeddings

APP_CODE = "cityeyeprod"
COMPOUND_ID = 17

docs = []
for language in ["en", "ar"]:
    content = get_compound_content(APP_CODE, COMPOUND_ID, language)
    docs += build_documents(content, APP_CODE, language)

print(len(docs), "documents")

QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    url=settings.qdrant_url,
    collection_name=COLLECTION_NAME,
    force_recreate=True,
)
print("done")




from collections import Counter

print(Counter((d.metadata["language"], d.metadata["section"]) for d in docs))

for lang in ["en", "ar"]:
    for section in ["faq", "communityRules", "termsConditions"]:
        first = next(
            (d for d in docs if d.metadata["language"] == lang and d.metadata["section"] == section),
            None,
        )
        print(lang, section, "→", first.page_content[:60] if first else "❌ مفيش")
        