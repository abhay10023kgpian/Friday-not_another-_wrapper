from connections import engine
from sqlalchemy import text

def check_database_connection():
    sql_query = """ALTER SYSTEM SET wal_level = logical;
                ALTER SYSTEM SET max_wal_senders = 10;
                ALTER SYSTEM SET max_replication_slots = 10;
                """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        return {"database": result.scalar()}

    except Exception as e:
        return {
            "database": "Disconnected",
            "error": str(e)
        }
        
if __name__ == "__main__":
    result = check_database_connection()
    print(result)
