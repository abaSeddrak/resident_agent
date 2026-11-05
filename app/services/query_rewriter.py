from app.models.chat import PreMessages
from app.prompts.rewrite_prompt import REWRITE_PROMPT
from langchain_openai import ChatOpenAI

from app.config import settings

llm_reqritw = ChatOpenAI(
    model= settings.openai_model,
    api_key=settings.openai_api_key,
)
def rewrite_question(question:str,history:list[PreMessages]):
    if not history:
        return question
    history_text = " ".join(f"{m.role}  {m.content }" for m in history)

       
    pro =REWRITE_PROMPT.format(history=history_text,question=question)
    full = llm_reqritw.invoke(pro).content
    return full


if __name__ == "__main__":
    history = [
        PreMessages(role="user", content="اوقات الهدوء في الكمبوند؟"),
        PreMessages(role="assistant", content="ساعات الهدوء يوميًا من 11 مساءً حتى 8 صباحًا، ويوم الجمعة حتى 11 صباحًا."),
    ]
    print(rewrite_question("ويوم السبت؟", history))
    print(rewrite_question("ايه رسوم الصيانة؟", history))
    print(rewrite_question("ويوم السبت؟", []))


