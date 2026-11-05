from fastapi import FastAPI
from app.models.chat import ChatRequest
from app.services.chat_service import answer
from app.models.chat import ChatResult,ChatResponse
from app.guardrails.pii import redact_pii
app = FastAPI(title="Chatbot")

@app.post("/chat")
def chat(request:ChatRequest):
    reply =answer(redact_pii(request.question),request.history , request.app_code,request.compound_id,request.language_code,
                  langsmith_extra={
                    "metadata":{
                        "app_code":request.app_code,
                        "compound_id":request.compound_id,
                        "language_code":request.language_code   
                    }
                  }
                  )
    return ChatResponse(answer=reply.answer)