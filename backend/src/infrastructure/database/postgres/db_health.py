from connections import engine
from sqlalchemy import text

def check_database_connection():
    sql_query = """
    INSERT INTO products (
    product_name, product_id, brand_name, price, color, size
    )
    VALUES
    
    ('Air Max 90', 'n-a-01fab12', 'Nike', 130.00, 'White/Black', '10')
    
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("select * from products;"))

        return {"database": result.scalar()}

    except Exception as e:
        return {
            "database": "Disconnected",
            "error": str(e)
        }
        
if __name__ == "__main__":
    result = check_database_connection()
    print(result)
