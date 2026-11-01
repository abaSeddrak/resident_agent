import json

from app.services.chat_service import answer

with open("evals/golden_set.json", "r", encoding="utf-8") as file:
    cases = json.load(file)

for case in cases:
    result = answer(
        case["question"],
        case["app_code"],
        case["compound_id"],
        case["language_code"],
    )

    if case["type"] == "answerable":
        section_hit = case["expected_section"] in result.sections
    else:
        section_hit = None

    print(
        f"{case['id']:<14} "
        f"section_hit={str(section_hit):<6} "
        f"sections={result.sections}"
    )
    print(f"    answer: {result.answer[:80]}")