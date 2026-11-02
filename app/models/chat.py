from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question:str = Field(min_length=1, max_length=500)
    app_code:str
    compound_id:int
    language_code:str
    

class ChatResponse(BaseModel):
    answer:str
    
    
class ChatResult(BaseModel):
    answer:str
    contexts:list[str]
    sections:list[str]
    
    
    