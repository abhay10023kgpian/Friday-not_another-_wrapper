from connections import engine
from sqlalchemy import text

def check_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "Connected"}

    except Exception as e:
        return {
            "database": "Disconnected",
            "error": str(e)
        }
        
if __name__ == "__main__":
    result = check_database_connection()
    print(result)
