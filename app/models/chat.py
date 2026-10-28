from pydantic import BaseModel

class ChatRequest(BaseModel):
    question:str
    app_code:str
    compound_id:int
    language_code:str
    

class ChatResponse(BaseModel):
    answer:str