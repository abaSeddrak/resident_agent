REWRITE_PROMPT = """Given the conversation history and a follow-up question, rewrite the follow-up question into a standalone question that can be understood without the history.

Rules:
- Keep the same language as the follow-up question.
- If the follow-up question is already standalone, return it unchanged.
- Return ONLY the rewritten question, nothing else.
- Do NOT answer the question.

Conversation history:
{history}

Follow-up question: {question}

Standalone question:"""