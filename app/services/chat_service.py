from langchain_openai import ChatOpenAI
from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.services.text_cleaning import html_to_text
from app.clients.cityeye_client import get_compound_content
llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)


def answer(question: str,appCode: str, compoundId: int, language_code: str):
    
    content = get_compound_content(appCode,compoundId,language_code)
    full_content = ""
    for key, value in content.items():  # .items unpacking two key and values
           full_content += f"## {key}\n {html_to_text(value)}\n\n"
    llm_answer = llm.invoke(SYSTEM_PROMPT.format(question=question,content=full_content)).content
    return llm_answer
