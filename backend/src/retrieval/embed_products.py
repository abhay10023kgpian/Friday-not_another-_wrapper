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
    

def fetch_products():
    sql_query = text("SELECT * FROM products")
    with engine.connect() as connection:
        result = connection.execute(sql_query)
        products = [transform_product(row) for row in result.mappings()]
    return products

def chunk(products=None):
    #convert products into documents for embedding
    
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

    
class ProductEmbedder:
    def __init__(self, index_name : str = "product-documents"):
        
        self.vector_store = getStore(index_name)
        
        print("store created/loaded successfully")

    def embed_products(self):
        print("Fetching products from the database...")
        
        transformed_products = fetch_products()
        
        print(f"Fetched {len(transformed_products)} products.")
        
        chunked_docs = chunk(transformed_products)
        
        print(f"Fetched {len(chunked_docs)} products.")
        
        self.vector_store.add_documents(chunked_docs)
        
        print("Successfully indexed products into the vector store!")
        
        
    def kafka_embed_products(self, raw_products): ##used by kafka
        
        transformed_products = [transform_product(row) for row in raw_products]
        chunked_docs = chunk(transformed_products)
        
        print(f"Fetched {len(chunked_docs)} products through kafka.")

        self.vector_store.add_documents(chunked_docs)

        print("Successfully indexed products into the vector store!")
        
        
if __name__ == "__main__":
    embedder = ProductEmbedder()
    print(embedder.embed_products())