from fastapi import FastAPI
from app.models.chat import ChatRequest
from app.services.chat_service import answer
app = FastAPI(title="Chatbot")

@app.post("/chat")
def chat(request:ChatRequest):
    reply =answer(request.question,request.app_code,request.compound_id,request.language_code)
    return reply