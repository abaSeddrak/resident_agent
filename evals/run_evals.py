import json
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from app.config import settings
from app.services.chat_service import answer
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from app.models.chat import PreMessages
from ragas.metrics import(
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
    ResponseRelevancy

)

with open("evals/golden_set.json", "r", encoding="utf-8") as file:
    cases = json.load(file)
ragas_samples = []
judge_llm = LangchainLLMWrapper(ChatOpenAI( model=settings.openai_model, api_key=settings.openai_api_key,temperature=0))
judge_embeddings = LangchainEmbeddingsWrapper(
    OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)
)
for case in cases:
    history = [PreMessages(**m) for m in case.get("history", [])]
    result = answer(
        
        question=case["question"],
        history=history,
        appCode=case["app_code"],
        compoundId=case["compound_id"],
        language_code=case["language_code"],
    )

    if case["type"] == "answerable":
        section_hit = case["expected_section"] in result.sections
        ragas_samples.append({
           "user_input": case["question"],
           "response": result.answer,
           "retrieved_contexts":result.contexts,
           "reference": case["expected_answer"],
        })
    else:
        section_hit = None

    print(
        f"{case['id']:<14} "
        f"section_hit={str(section_hit):<6} "
        f"sections={result.sections}"
    )
    print(f"    answer: {result.answer[:80]}")
dataset = EvaluationDataset.from_list(ragas_samples)

print(dataset)
print(f" len {len(ragas_samples)}")

rags_result = evaluate(
    dataset=dataset,
    llm=judge_llm,
    embeddings=judge_embeddings,
    metrics=[
        Faithfulness(),
        LLMContextPrecisionWithReference(),
        LLMContextRecall(), 
        ResponseRelevancy()
    ]
)

print(rags_result)