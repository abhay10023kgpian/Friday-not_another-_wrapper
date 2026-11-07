from connections import engine
from sqlalchemy import text

def insert_to_db():
    # read the sql query from the file migrations 002
    with open("src/infrastructure/database/postgres/migrations/002_insert.up.sql", "r") as f:
        sql_query = f.read()
    try:
        # engine.begin() automatically commits the INSERT transaction
        with engine.begin() as connection:
            connection.execute(text(sql_query))
            total_count = connection.execute(text("SELECT COUNT(*) FROM products;")).scalar()

        return {
            "status": "Success",
            "total_products_in_db": total_count
        }

    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e)
        }
        
if __name__ == "__main__":
    result = insert_to_db()
    print(result)