
from langchain_core.documents import Document

from app.services.text_cleaning import html_to_text

SEPARATORS = {
    "faq": "####",
    "communityRules": "⸻",
    "termsConditions": "⸻",
    "aboutUs": None,
    "bankInfo": None,
}


def build_documents(content: dict[str, str], app_code: str, language_code: str) -> list[Document]:
    docs = []
    for key, separator in SEPARATORS.items():
        text = html_to_text(content[key])
        if not text:
            continue

        chunks = split_by_separator(text, separator) if separator else [text]
        for chunk in chunks:
            docs.append(Document(
                page_content=chunk,
                metadata={"app_code": app_code, "section": key, "language": language_code},
            ))
    return docs

def split_by_separator(text:str,separator:str)-> list[str]:
    parts =  text.split(separator)
    chunks = [part.strip() for part in parts if part.strip()]
    print(len(chunks))
    return chunks
  
    
    