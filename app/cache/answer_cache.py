import uuid

from app.cache.normalize import normalize_question

CACHE_NAMESPACE = uuid.UUID("6f1c2a4e-8b3d-4c7a-9e21-5d0f3b8a7c14")


def make_cache_id(app_code: str, language_code: str, question: str) -> str:
    key = f"{app_code}|{language_code}|{normalize_question(question)}"
    return str(uuid.uuid5(CACHE_NAMESPACE, key))