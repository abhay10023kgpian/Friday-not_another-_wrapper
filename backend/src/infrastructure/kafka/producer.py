from confluent_kafka import Producer
import json

class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        bootstrap_config = {'bootstrap.servers': bootstrap_servers}
        self.producer = Producer(bootstrap_config)
    
    def produce(self, topic: str, event : dict):
        
        value = json.dumps(event).encode('utf-8')
        
        print(f"Producing event to topic {topic}: {value}, to bootstrap servers: {self.producer.list_topics().brokers}")
        
        self.producer.produce(topic, value)
        self.producer.flush()
        
        
        
def produce_event(bootstrap_servers: str, topic: str, event: dict):
    producer = KafkaProducer(bootstrap_servers)
    producer.produce(topic, event)
    
if __name__ == "__main__":
    bootstrap_servers = "localhost:9092"
    topic = "shoes"
    event = {"key": "nice"}
    
    produce_event(bootstrap_servers, topic, event)