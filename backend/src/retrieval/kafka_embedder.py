from src.retrieval.vector_store import getStore
from src.infrastructure.kafka.consumer import KafkaConsumer
from src.retrieval.embed_products import ProductEmbedder
import os

def generate_embeddings():
    bootstrap_servers = os.getenv("bootstrap_servers")
    group_id = os.getenv("group_id")
    topics = ["ragdb.public.products"]
    
    consumer = KafkaConsumer(bootstrap_servers, group_id, topics)
    embedder = ProductEmbedder(index_name="product-documents")
    
    for event in consumer.consume():
        print(100*"-")
        print(100*"-")
        print(100*"-")
        
        print(f"Consumed event: {event}")
        # new line added to check for create or update operations 
        print(100*"-")
        
        if event.get("op") in ["c", "u"]:  # Check for create or update operations
            
            print(f"create/update operation: {event.get('op')}")
            print(100*"-")
            
            data = event.get("after")
            
            
            if data:
                print(f"New/Updated product data: {data}")
                
                print("Generating embeddings for the new/updated product...")
                
                #put raw data
                
                embedder.kafka_embed_products([data])
                print("Embeddings generated successfully.")


if __name__ == "__main__":
    print("Starting the embedding generation process...")
    generate_embeddings()
    

# ----------------------------------------------------------------------------------------------------
# {'before': None, 'after': {'id': 44, 'product_name': 'Air Max 90', 'product_id': 'n-a-01ab14', 'brand_name': 'Nike', 'price': 130.0, 'color': 'White/Black', 'size': '10'}, 'source': {'version': '3.3.2.Final', 'connector': 'postgresql', 'name': 'ragdb', 'ts_ms': 1794059610471, 'snapshot': 'false', 'db': 'ragdb', 'sequence': '["26893736","26893792"]', 'ts_us': 1794059610471975, 'ts_ns': 1794059610471975000, 'schema': 'public', 'table': 'products', 'txId': 774, 'lsn': 26893792, 'xmin': None}, 'transaction': None, 'op': 'c', 'ts_ms': 1794059610754, 'ts_us': 1794059610754070, 'ts_ns': 1794059610754070594}