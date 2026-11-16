from datetime import datetime, timedelta, timezone

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.cache.cache_key import make_cache_id
from app.config import settings

CACHE_COLLECTION = "answer_cache"
CACHE_TTL = timedelta(hours=24)

client = QdrantClient(url=settings.qdrant_url)


def ensure_cache_collection():
    if not client.collection_exists(CACHE_COLLECTION):
        client.create_collection(
            collection_name=CACHE_COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )


def get_cached_answer(app_code: str, language_code: str, question: str) -> str | None:
    points = client.retrieve(
        collection_name=CACHE_COLLECTION,
        ids=[make_cache_id(app_code, language_code, question)],
    )
    if not points:
        return None

    payload = points[0].payload
    created_at = datetime.fromisoformat(payload["created_at"])
    if datetime.now(timezone.utc) - created_at > CACHE_TTL:
        return None

    return payload["answer"]