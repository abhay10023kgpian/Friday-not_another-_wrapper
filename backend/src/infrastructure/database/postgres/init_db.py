from pathlib import Path
from sqlalchemy import text

from src.infrastructure.database.postgres.connections import admin_engine as engine

def init_db():
    # Load the SQL file
    migration_file = (
    Path(__file__).resolve().parent
    / "migrations"
    / "001_init.up.sql"
    )
    sql_file = migration_file.read_text(encoding="utf-8")

    # engine.begin() auto-commits the CREATE and INSERT statements
    with engine.begin() as connection:
        connection.execute(text(sql_file))
        print("Table created and test data inserted!")

    # Verify by querying the data - select last 5 data
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM products ORDER BY id DESC LIMIT 5;"))
        for row in result.mappings():
            print(dict(row))

def add_access_control():
    # Load the SQL file
    migration_file = (
    Path(__file__).resolve().parent
    / "migrations"
    / "003_create_llm_user.up.sql"
    )
    sql_file = migration_file.read_text(encoding="utf-8")

    # engine.begin() auto-commits the CREATE and INSERT statements
    with engine.begin() as connection:
        connection.execute(text(sql_file))
        print("Access control table created and test data inserted!")
        
if __name__ == "__main__":
    init_db()
    add_access_control()