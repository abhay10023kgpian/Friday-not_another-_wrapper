import os
from dotenv import load_dotenv
from typing import Literal

from vector_store import getStore
from src.nlp.text_to_sql import get_query_generation_prompt, execute_sql_query


load_dotenv()

vector_store = getStore("product-documents")

# vector_store.add_documents(docs)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

from typing import List, Literal
import os

from pydantic import BaseModel, Field

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from langgraph.graph import StateGraph, START, END
from src.retrieval.model import State, get_llm

llm = get_llm()

def hybrid_retriever(State):
    q = State["question"]
    return {"docs" : retriever.invoke(q)}

decide_tool_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a query router. Reply with exactly one word, nothing else."
        ),
        HumanMessage(
            content=(
                "Our store DB has a 'products' table with columns: id, product_name, product_id, brand_name, price, color, size.\n\n"
                "sql_retriever = price, brand, size, color, list, filter, count, sort, cheapest, expensive, specific product lookup\n"
                "hybrid_retriever = recommendations, vague descriptions, company policy, fuzzy/partial match\n"
                "generate_direct = chitchat, greetings, general knowledge, harmful SQL\n\n"
                "shoes under 80 → sql_retriever\n"
                "Nike shoes → sql_retriever\n"
                "cheapest shoe → sql_retriever\n"
                "size 9 shoes → sql_retriever\n"
                "black shoes → sql_retriever\n"
                "most expensive shoe → sql_retriever\n"
                "Adidas between 100 and 150 → sql_retriever\n"
                "kids shoes in stock → sql_retriever\n"
                "comfortable running shoes → hybrid_retriever\n"
                "return policy → hybrid_retriever\n"
                "how to clean shoes → generate_direct\n"
                "hello → generate_direct\n\n"
                "Question: {question}\n"
                "Answer:"
            )
        ),
    ]
)

VALID_TOOLS = {"sql_retriever", "hybrid_retriever", "generate_direct"}

def decide_tool(state: State):
    response = llm.invoke(
        decide_tool_prompt.format_messages(question=state["question"])
    )
    text = response.content.strip().lower()

    for tool in ["sql_retriever", "hybrid_retriever", "generate_direct"]:
        if tool in text:
            return {"tool_selected": tool}

    return {"tool_selected": "hybrid_retriever"}


class RelvenceDecision(BaseModel):
    is_relevant: bool = Field(description="True if the document helps answer the question, else False.")

is_relevant_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are judging document relevance.\n"
                "Return JSON that matches this schema:\n"
                "{{'is_relevant': boolean}}\n\n"
                "A document is relevant if it contains information useful for answering the question."
            )
        ),
        HumanMessage(content="Question:\n{question}\n\nDocument:\n{document}"),
    ]
)

relvenceLLM = llm.with_structured_output(RelvenceDecision, method="json_mode")

def is_relevent(state: State):
    relevent_docs: List[Document] = []

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
        SystemMessage(
            content=(
                "Answer the question using only your general knowledge.\n"
                "Do NOT assume access to external documents.\n"
                "If you are unsure or the answer requires specific sources, say:\n"
                "'I don't know based on my general knowledge.'"
            )
        ),
        HumanMessage(content="{question}"),
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

def route_after_decision(state : State) -> Literal["hybrid_retriever", "generate_direct", "sql_retriever"]:
    if state["tool_selected"] == "hybrid_retriever":
        return "hybrid_retriever"
    elif state["tool_selected"] == "sql_retriever":
        return "sql_retriever"
    return "generate_direct"

rag_generation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a business RAG assistant.\n"
                "Answer the user's question using ONLY the provided context.\n"
                "If the context does not contain enough information, say:\n"
                "'No relevant document found.'\n"
                "Do not use outside knowledge.\n"
            )
        ),
        HumanMessage(
            content=(
                "Question:\n{question}\n\n"
                "Context:\n{context}\n"
            )
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

def sql_retriever(state: State):
    
    query_prompt = get_query_generation_prompt()
    sql_query = llm.invoke(
        query_prompt.format_messages(user_input=state["question"])
    ).content

    rows = execute_sql_query(sql_query)
    docs = [Document(page_content=str(row)) for row in rows]

    return {"docs": docs}

def build_graph():
    graph = StateGraph(State)
    graph.add_node("hybrid_retriever", hybrid_retriever)
    graph.add_node("sql_retriever", sql_retriever)
    graph.add_node("decide_tool", decide_tool)
    
    graph.add_node("generate_direct", generate_direct)
    graph.add_node("is_relevant", is_relevent)
    graph.add_node("generate_from_context", generate_from_context)


    graph.add_edge(START, "decide_tool")
    graph.add_conditional_edges("decide_tool", route_after_decision, {
        "generate_direct": "generate_direct",
        "hybrid_retriever": "hybrid_retriever",
        "sql_retriever": "sql_retriever"
    })

    graph.add_edge("hybrid_retriever", "is_relevant")
    graph.add_edge("sql_retriever", "is_relevant")
    
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
        
        res = app.invoke({"question": question,"tool_selected": "generate_direct", "docs": [], "relevant_docs":[], "answer": ""})
        print(f"Question: {res['question']}")
        print(100*"-")
        print("Answer:", res["answer"])
        print(100*"-")
        print("Tool Selected:", res.get("tool_selected"))
        print(100*"-")
        print("Docs:", res["docs"])
        print(100*"-")
        print("Relevant Docs:", res.get("relevant_docs", "No relevant docs available"))
        print(100*"-")
        print("Context:", res.get("context", "No context available"))
        print(100*"-")

    
if __name__ == "__main__":
    chatbot()
    # print(build_graph())
    # print(decide_tool({"question": "I want nike white shoes of size 4","tool_selected": "generate_direct", "docs": [], "relevant_docs":[], "answer": ""}))