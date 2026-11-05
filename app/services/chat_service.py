from langchain_openai import ChatOpenAI
from langsmith import traceable
from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.rag.retriever import retrieve
from app.models.chat import ChatResult
from app.guardrails.output_rails import check_answer
from app.models.chat import PreMessages
import logging
from app.services.query_rewriter import rewrite_question
logger = logging.basicConfig(level=logging.DEBUG)
llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)

@traceable(name="resident-chat-answer")
def answer(question: str, history:list[PreMessages],  appCode: str, compoundId: int, language_code: str)->ChatResult:
   
    standalone_question = rewrite_question(question,history)
    docs = retrieve(standalone_question, appCode, language_code, 4)
    
   
    for h in history:
     logging.info(h.role)

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
    return ChatResult(
        answer=llm_answer,
        contexts=[doc.page_content for doc in docs],
        sections=[doc.metadata["section"] for doc in docs],
    )