from confluent_kafka import Consumer, KafkaError
import json

class KafkaConsumer:
    def __init__(self, bootstrap_servers : str, group_id: str, topics: list):
        bootstrap_config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        
        self.consumer = Consumer(bootstrap_config)
        self.consumer.subscribe(topics)
        
    def  consume(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer error: {msg.error()}")
                        continue
                
                event = json.loads(msg.value().decode('utf-8'))
                yield event
        except KeyboardInterrupt:
            print("gracefully stopping tracking")
        finally:
            self.consumer.close()
            
if __name__ == "__main__":
    bootstrap_servers = "localhost:9092"
    group_id = "my_group"
    topics = ["ragdb.public.products"]
    
    consumer = KafkaConsumer(bootstrap_servers, group_id, topics)
    
    for event in consumer.consume():
        print(f"Consumed event: {event}")