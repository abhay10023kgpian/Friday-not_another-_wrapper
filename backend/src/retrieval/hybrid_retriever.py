import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.retrievers import PineconeHybridSearchRetriever
from vector_store import getStore


load_dotenv()

vector_store = getStore("product-documents")

# vector_store.add_documents(docs)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

from typing import List, TypedDict, Literal
import time
import os

from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question : str
    need_retrieval: bool

    docs : list[Document]
    relevant_docs : list[Document]

    context: str
    answer : str

llm = ChatGroq(
    model="openai/gpt-oss-120b", 
    temperature=0.2,
    max_tokens=800
)

def retrieve(State):
    q = State["question"]
    return {"docs" : retriever.invoke(q)}

class RetrieveDecision(BaseModel):
    should_retrieve: bool = Field(
        ...,
        description="True if external documents are needed to answer reliably, else False."
    )
    
decide_retrieval_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You decide whether retrieval is needed.\n"
            "Return JSON that matches this schema:\n"
            "{{'should_retrieve': boolean}}\n\n"
            "Guidelines:\n"
            "- should_retrieve=True if answering requires specific facts, citations, or info likely not in the model.\n"
            "- should_retrieve=False for general explanations, definitions, or reasoning that doesn't need sources.\n"
            "- If unsure, choose True."
        ),
        ("human", "Question: {question}"),
    ]
)

should_retrieve_llm = llm.with_structured_output(RetrieveDecision)

def decide_retrieval(state: State):
    decision: RetrieveDecision = should_retrieve_llm.invoke(
        decide_retrieval_prompt.format_messages(question=state["question"])
    )
    return {"need_retrieval": decision.should_retrieve}

class RelvenceDecision(BaseModel):
    is_relevant : bool = Field(description="True if the document helps answer the question, else False.")

is_relevant_prompt = ChatPromptTemplate.from_messages(
    [   
        (
            "system",
            "You are judging document relevance.\n"
            "Return JSON that matches this schema:\n"
            "{{'is_relevant': boolean}}\n\n"
            "A document is relevant if it contains information useful for answering the question."
        ),
        (
            "human",
            "Question:\n{question}\n\nDocument:\n{document}"
        )
    ]
)

relvenceLLM = llm.with_structured_output(RelvenceDecision)

def is_relevent(state : State):
    relevent_docs : List[Document] = []

    for doc in state["docs"]:
        out = relvenceLLM.invoke(
            is_relevant_prompt.format_messages(
                question=state["question"],
                document=doc.page_content
            )
        )

        if out.is_relevant:
            relevent_docs.append(doc)
    
    return {"relevant_docs": relevent_docs} 

# res = (is_relevant_prompt | relvenceLLM).invoke({"question":"hi","document": "doc"})

direct_generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the question using only your general knowledge.\n"
            "Do NOT assume access to external documents.\n"
            "If you are unsure or the answer requires specific sources, say:\n"
            "'I don't know based on my general knowledge.'"
        ),
        ("human", "{question}"),
    ]
)


def generate_direct(state: State):
    out = llm.invoke(
        direct_generation_prompt.format_messages(
            question=state["question"]
        )
    )
    return {
        "answer": out.content
    }

def route_after_decision(state : State) -> Literal["retrieve", "generate_direct"]:
    if state["need_retrieval"]:
        return "retrieve"
    return "generate_direct"

rag_generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a business RAG assistant.\n"
            "Answer the user's question using ONLY the provided context.\n"
            "If the context does not contain enough information, say:\n"
            "'No relevant document found.'\n"
            "Do not use outside knowledge.\n"
        ),
        (
            "human",
            "Question:\n{question}\n\n"
            "Context:\n{context}\n"
        ),
    ]
)

def generate_from_context(state: State):
    # Stuff relevant docs into one block
    context = "\n\n---\n\n".join(
        [d.page_content for d in state.get("relevant_docs", [])]
    ).strip()

    if not context:
        return {"answer": "No relevant document found.", "context": ""}

    out = llm.invoke(
        rag_generation_prompt.format_messages(
            question=state["question"],
            context=context
        )
    )
    return {"answer": out.content, "context": context}

def build_graph():
    graph = StateGraph(State)
    graph.add_node("retrieve", retrieve)

    graph.add_node("decide_retrieval", decide_retrieval)

    graph.add_node("generate_direct", generate_direct)
    graph.add_node("is_relevant", is_relevent)
    graph.add_node("generate_from_context", generate_from_context)


    graph.add_edge(START, "decide_retrieval")
    graph.add_conditional_edges("decide_retrieval", route_after_decision,{
        "generate_direct":"generate_direct",
        "retrieve": "retrieve"
    }
    )

    graph.add_edge("retrieve", "is_relevant")
    graph.add_edge("is_relevant", "generate_from_context")
    graph.add_edge("generate_from_context", END)
    graph.add_edge("generate_direct", END)

    app = graph.compile()
    
    return app


def generate_answer(question: str):
    app = build_graph()
    res = app.invoke(question)
    return res
# res = app.invoke({"question": "I want nike white shoes of size 4","need_retrieval": 0, "docs": [], "relevant_docs":[], "answer": ""})

def chatbot():
    
    app = build_graph()
    
    print("Welcome to the RAG Chatbot! Type your questions below.")
    
    while True:
        print(100*"-")
        print(100*"-")
        
        question = input("Enter your next question (or 'exit' to quit): ")

        if question.lower() == 'exit':
            break
        
        res = app.invoke({"question": question,"need_retrieval": 0, "docs": [], "relevant_docs":[], "answer": ""})
        print(f"Question: {res['question']}")
        print(100*"-")
        print("Answer:", res["answer"])
        print(100*"-")
        print("Need Retrieval:", res["need_retrieval"])
        print(100*"-")
        print("Docs:", res["docs"])
        print(100*"-")
        print("Relevant Docs:", res.get("relevant_docs", "No relevant docs available"))
        print(100*"-")
        print("Context:", res.get("context", "No context available"))
        print(100*"-")

    
if __name__ == "__main__":
    chatbot()