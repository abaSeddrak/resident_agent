from langchain_openai import ChatOpenAI
from langsmith import traceable
from app.config import settings
from app.models.chat import PreMessages
from app.prompts.rewrite_prompt import REWRITE_PROMPT

rewrite_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=settings.openai_api_key,
)


@traceable(name="query-rewrite")
def rewrite_question(question: str, history: list[PreMessages]) -> str:
    if not history:
        return question

    history_text = "\n".join(f"{m.role}: {m.content}" for m in history)
    prompt = REWRITE_PROMPT.format(history=history_text, question=question)
    rewritten = rewrite_llm.invoke(prompt).content
    return rewritten.strip()


if __name__ == "__main__":
    history = [
        PreMessages(role="user", content="اوقات الهدوء في الكمبوند؟"),
        PreMessages(role="assistant", content="ساعات الهدوء يوميًا من 11 مساءً حتى 8 صباحًا، ويوم الجمعة حتى 11 صباحًا."),
    ]
    print(rewrite_question("ويوم السبت؟", history))
    print(rewrite_question("ايه رسوم الصيانة؟", history))
    print(rewrite_question("ويوم السبت؟", []))