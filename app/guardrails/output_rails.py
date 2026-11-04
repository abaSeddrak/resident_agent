from nemoguardrails import RailsConfig, LLMRails
from langsmith import traceable

config = RailsConfig.from_path("app/guardrails/nemo")
rails = LLMRails(config)

NEMO_REFUSAL = "I'm sorry, I can't respond to that."

REFUSAL_MESSAGES = {
    "ar": "عذراً، لا أستطيع الإجابة على هذا السؤال حالياً. برجاء التواصل مع إدارة الكمبوند.",
    "en": "Sorry, I can't answer that right now. Please contact the compound management.",
}


@traceable(name="output-guard")
def check_answer(question: str, answer: str, chuncks: list[str], language_code: str):
    messages = [
        {"role": "context", "content": {
            "relevant_chunks": "\n".join(chuncks),
            "check_facts": True,
        }},
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
    result = rails.generate(messages=messages, options={"rails": ["output"]})
    content = result.response[-1]["content"]

    if content.strip() == NEMO_REFUSAL:
        return REFUSAL_MESSAGES.get(language_code, REFUSAL_MESSAGES["en"])
    return content


if __name__ == "__main__":
    chunks = ["رسوم الصيانة الشهرية للشقة 1500 جنيه"]
    print(check_answer("الرسوم كام؟", "الرسوم 1500 جنيه", chunks, "ar"))
    print(check_answer("الرسوم كام؟", "الرسوم 3000 جنيه", chunks, "ar"))