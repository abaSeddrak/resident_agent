from nemoguardrails import RailsConfig, LLMRails
from langsmith import traceable

config = RailsConfig.from_path("app/guardrails/nemo")
rails = LLMRails(config)

@traceable(name="output-guard")
def check_answer(question: str, answer: str, chuncks: list[str]):
    messages = [
        {"role": "context", "content":{
            "relevant_chunks":"\n".join(chuncks),
            "check_facts":True
            
            }},
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
    result = rails.generate(messages=messages,options={"rails": ["output"]})
  
    return result.response[-1]["content"]



if __name__ == "__main__":
    chunks = ["رسوم الصيانة الشهرية للشقة 1500 جنيه"]
    print(check_answer("الرسوم كام؟", "الرسوم 1500 جنيه", chunks))
    print(check_answer("الرسوم كام؟", "الرسوم 3000 جنيه", chunks))
