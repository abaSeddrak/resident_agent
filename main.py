import httpx
from markdownify import markdownify
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="Chatbot-City-Eye")
llm = ChatOpenAI(model="gpt-4o-mini")




