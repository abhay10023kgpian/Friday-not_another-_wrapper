from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from src.infrastructure.database.postgres.connections import engine
from sqlalchemy import text
from src.retrieval.model import get_llm
#prompt to generate sql query from natural language with strict system message that no delete update operations are allowed and only select queries are allowed
query_generation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are a helpful assistant that generates only SELECT SQL queries. Do not generate any DELETE, UPDATE, or INSERT queries
            . table_name(consisting only shoes) is 'products' with columns: id, product_name, product_id, brand_name, price, color, size.
            generate final query without any extra explanation or comments. this query will directly be executed on the database, so ensure it is syntactically.
            always fetch top 5 results unless mentioned, if price - order by desc.
            if invalid operation is requested, return "select 1;"
            """       
        ),
        HumanMessagePromptTemplate.from_template("{user_input}")
    ]
)

def get_query_generation_prompt() -> ChatPromptTemplate:
    return query_generation_prompt

def execute_sql_query(query: str):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = [dict(row) for row in result.mappings()]
    return rows

def debug_sql_query():
    quesiton = "I want to insert a new product into the products table with product_name 'Nike Air Max', product_id '12345', brand_name 'Nike', price 150, color 'Red', size 10. Please provide the SQL query for this operation."
    
    query_prompt = get_query_generation_prompt()
    llm = get_llm()
    query = llm.invoke(
        query_prompt.format_messages(user_input=quesiton)
    ).content
    
    print(query)

    # rows = execute_sql_query(query)
        
    # print(rows)
    
if __name__ == "__main__":
    debug_sql_query()