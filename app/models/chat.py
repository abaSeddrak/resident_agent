from pydantic import BaseModel, Field
from typing import Literal
class PreMessages(BaseModel):
    role:Literal["user","assistant"]
    content:str

class ChatRequest(BaseModel):
    question:str = Field(min_length=1, max_length=500)
    history:list[PreMessages]= []
    app_code:str
    compound_id:int
    language_code:str
    

class ChatResponse(BaseModel):
    answer:str
    
    
class ChatResult(BaseModel):
    answer:str
    contexts:list[str]
    sections:list[str]
    
    

