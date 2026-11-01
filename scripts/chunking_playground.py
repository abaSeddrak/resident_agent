from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import models

from app.clients.cityeye_client import get_compound_content
from app.config import settings
from app.rag.chunking import split_by_separator
from app.services.text_cleaning import html_to_text

APP_CODE = "cityeyeprod"
COMPOUND_ID = 17
LANGUAGE_CODE = "en"

SEPARATORS = {
    "faq": "####",
    "communityRules": "⸻",
    "termsConditions": "⸻",
    "aboutUs": None,
    "bankInfo": None,
}

# 1. Fetch the compound content
content = get_compound_content(APP_CODE, COMPOUND_ID, LANGUAGE_CODE)

# 2. Chunk every section and wrap each chunk in a Document
docs = []
for key, separator in SEPARATORS.items():
    text = html_to_text(content[key])
    if not text:
        continue

    if separator:
        chunks = split_by_separator(text, separator)
    else:
        chunks = [text]

    for chunk in chunks:
        docs.append(Document(
            page_content=chunk,
            metadata={"app_code": APP_CODE, "section": key, "language": LANGUAGE_CODE},
        ))

print("documents:", len(docs))

# 3. Embed and store in Qdrant
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)

vector_store = QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="compound_content",
    force_recreate=True,
)

# 4. Search only inside this compound
tenant_filter = models.Filter(
    must=[models.FieldCondition(key="metadata.app_code", match=models.MatchValue(value=APP_CODE))]
)

for question in ["how can I add a guest?", "what is the speed limit?", "how do I pay?"]:
    print("\nQ:", question)
    results = vector_store.similarity_search_with_score(question, k=2, filter=tenant_filter)
    for doc, score in results:
        print(f"  {score:.3f} [{doc.metadata['section']}] {doc.page_content[:70]!r}")