from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from sqlalchemy import text
from src.retrieval.model import get_llm
from src.infrastructure.database.postgres.connections import get_connection
#prompt to generate sql query from natural language with strict system message that no delete update operations are allowed and only select queries are allowed
query_generation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are a helpful assistant that generates only SELECT SQL queries. Do not generate any DELETE, UPDATE, or INSERT queries
            . table_name(consisting only shoes) is 'products' with roughly,
                id PRIMARY KEY,
                product_name VARCHAR(255)
                product_id VARCHAR(255)
                brand_name VARCHAR(255)
                price DECIMAL(10, 2)
                color VARCHAR
                size VARCHAR
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
    try:
        with get_connection() as connection:
            result = connection.execute(text(query))
            rows = [dict(row) for row in result.mappings()]
            return rows
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return

def debug_sql_query():
    quesiton = "I want to insert a new product into the products table with product_name 'Nike Air Max', product_id '12345', brand_name 'Nike', price 150, color 'Red', size 10. Please provide the SQL query for this operation."
    
    query_prompt = get_query_generation_prompt()
    llm = get_llm()
    query = llm.invoke(
        query_prompt.format_messages(user_input=quesiton)
    ).content
    
    print(query)

    # rows = execute_sql_query("Select from products where id=460;")
    rows = execute_sql_query(query)
        
    print(rows)
    
if __name__ == "__main__":
    debug_sql_query()