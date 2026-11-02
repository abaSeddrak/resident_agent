from langchain_openai import ChatOpenAI
from langsmith import traceable
from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.rag.retriever import retrieve
from app.models.chat import ChatResult

llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)

@traceable(name="resident-chat-answer")
def answer(question: str, appCode: str, compoundId: int, language_code: str)->ChatResult:
    docs = retrieve(question, appCode, language_code, 4)
    if not docs:
        if language_code == "ar":
            return ChatResult(
                answer="معنديش المعلومة دي، من فضلك تواصل مع الإدارة من التطبيق.",
                contexts=[],
                sections=[],
            )
        return ChatResult(
            answer="I don't have this information. Please contact management through the app",
            contexts=[],
            sections=[],
        )

    context = "\n\n".join(
        f"## {doc.metadata['section']}\n{doc.page_content}" for doc in docs
    )

    llm_answer = llm.invoke(
        SYSTEM_PROMPT.format(question=question, content=context)
    ).content

    return ChatResult(
        answer=llm_answer,
        contexts=[doc.page_content for doc in docs],
        sections=[doc.metadata["section"] for doc in docs],
    )
