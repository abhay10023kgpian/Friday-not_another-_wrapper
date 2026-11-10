from langchain_groq import ChatGroq
from typing import Literal, TypedDict
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()

def get_llm() -> ChatGroq:
    llm = ChatGroq(
    model="openai/gpt-oss-120b", 
    temperature=0.2,
    max_tokens=800
    )
    return llm

class State(TypedDict):
    question : str
    tool_selected : Literal["sql_retriever", "hybrid_retriever", "generate_direct"]

    docs : list[Document]
    relevant_docs : list[Document]

    context: str
    answer : str
