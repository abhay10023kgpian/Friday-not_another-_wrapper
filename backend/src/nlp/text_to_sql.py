from langchain.messages import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from src.infrastructure.database.postgres.connections import engine

#prompt to generate sql query from natural language with strict system message that no delete update operations are allowed and only select queries are allowed
query_generation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant that generates only SELECT SQL queries. Do not generate any DELETE, UPDATE, or INSERT queries."
        ),
        HumanMessagePromptTemplate.from_template("{user_input}")
    ]
)

def get_query_generation_prompt() -> ChatPromptTemplate:
    return query_generation_prompt

def execute_sql_query(query: str):
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = [dict(row) for row in result.mappings()]
    return rows