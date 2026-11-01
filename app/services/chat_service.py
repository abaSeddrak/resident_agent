from langchain_openai import ChatOpenAI
from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.services.text_cleaning import html_to_text
from app.clients.cityeye_client import get_compound_content
from app.rag.retriever import retrieve
llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)


def answer(question: str,appCode: str, compoundId: int, language_code: str):
    docs = retrieve(question,appCode,language_code,4)
    if not docs:
        if language_code == "ar":
            return "معنديش المعلومة دي، من فضلك تواصل مع الإدارة من التطبيق."
        return "I don't have this information. Please contact management through the app."
   
    context = "\n\n".join(f"## {doc.metadata['section']}\n{doc.page_content}" for doc in docs)
    
    llm_answer = llm.invoke(SYSTEM_PROMPT.format(question=question,content=context)).content
    return llm_answer
