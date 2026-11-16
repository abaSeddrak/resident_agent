from langchain_openai import ChatOpenAI
from langsmith import traceable
from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.rag.retriever import retrieve
from app.models.chat import ChatResult
from app.guardrails.output_rails import check_answer
from app.models.chat import PreMessages
import logging
from app.cache.answer_cache import get_cached_answer, save_answer
from app.guardrails.output_rails import REFUSAL_MESSAGES

from app.services.query_rewriter import rewrite_question
from portkey_ai import PORTKEY_GATEWAY_URL,createHeaders
logger = logging.basicConfig(level=logging.DEBUG)

llm = ChatOpenAI(model=settings.openai_model, 
                 api_key=settings.portkey_api_key,
                 base_url=PORTKEY_GATEWAY_URL,
                 default_headers=createHeaders(
                     api_key=settings.portkey_api_key,
                     config= settings.portkey_config_id
                   
                 ),
                 )
@traceable(name="resident-chat-answer")
def answer(question: str, history: list[PreMessages], appCode: str, compoundId: int, language_code: str, use_cache: bool = True) -> ChatResult:
    standalone_question = rewrite_question(question, history)

    if use_cache:
        cached = get_cached_answer(appCode, language_code, standalone_question)
        if cached:
            return ChatResult(answer=cached, contexts=[], sections=[])

    docs = retrieve(standalone_question, appCode, language_code, 4)

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
        SYSTEM_PROMPT.format(question=standalone_question, content=context)
    ).content

    llm_answer = check_answer(standalone_question, llm_answer, [doc.page_content for doc in docs], language_code)

    if use_cache and llm_answer not in REFUSAL_MESSAGES.values():
        save_answer(appCode, language_code, standalone_question, llm_answer)

    return ChatResult(
        answer=llm_answer,
        contexts=[doc.page_content for doc in docs],
        sections=[doc.metadata["section"] for doc in docs],
    )