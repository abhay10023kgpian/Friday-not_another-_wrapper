from connections import engine
from sqlalchemy import text

def insert_to_db():
    sql_query = """
    INSERT INTO products (
        product_name, product_id, brand_name, price, color, size
    )
    VALUES (
        'Air Max 90', 'n-a-01aazb12', 'Nike', 130.991, 'White/Black', '10'
    )
    RETURNING product_id;
    """
    try:
        # engine.begin() automatically commits the INSERT
        with engine.begin() as connection:
            result = connection.execute(text(sql_query))
            inserted_id = result.scalar()

        return {"database": "Connected", "inserted_product_id": inserted_id}

    except Exception as e:
        return {
            "database": "Disconnected",
            "error": str(e)
        }
        
if __name__ == "__main__":
    result = insert_to_db()
    print(result)