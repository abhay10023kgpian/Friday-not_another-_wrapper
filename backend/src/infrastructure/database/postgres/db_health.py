from connections import engine
from sqlalchemy import text

def check_database_connection():
    sql_query = """SELECT 1;"""
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
