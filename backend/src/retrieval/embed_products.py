from src.infrastructure.database.postgres.connections import engine
from langchain_core.documents import Document
from sqlalchemy import text
from vector_store import getStore

def transform_product(row):
    content = (
        f"Product Name: {row['product_name']}. "
        f"Product ID: {row['product_id']}. "
        f"Brand: {row['brand_name']}. "
        f"Price: ${row['price']}. "
        f"Color: {row['color']}. "
        f"Size: {row['size']}."
    )

    return {
        "product_id": row["product_id"],
        "product_name": row["product_name"],
        "brand_name": row["brand_name"],
        "price": float(row["price"]),
        "color": row["color"],
        "size": row["size"],
        "content": content
    }
    
sql_query = text("SELECT * FROM products")

def fetch_products():
    with engine.connect() as connection:
        result = connection.execute(sql_query)
        products = [transform_product(row) for row in result.mappings()]
    return products

def chunk():
    #convert products into documents for embedding
    products = fetch_products()
    
    docs = [Document(
        page_content=product["content"],
        metadata={
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "brand_name": product["brand_name"],
            "price": product["price"],
            "color": product["color"],
            "size": product["size"]
        },
        id=product["product_id"]
    ) for product in products]

    return docs

def embed_products():
    print("Fetching products from the database...")
    docs = chunk()
    
    print(f"Fetched {len(docs)} products.")

    vector_store = getStore("product-documents")
    print("store created/loaded successfully")
    
    vector_store.add_documents(docs)

    print("Successfully indexed products into the vector store!")
    
if __name__ == "__main__":
    print(embed_products())