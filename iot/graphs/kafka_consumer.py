# myapp/kafka_consumer.py
from kafka import KafkaConsumer
import json
import threading

class KafkaMessageConsumer:
    def __init__(self, bootstrap_servers, topics, group_id):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def consume(self):
        for message in self.consumer:
            print(f"Received message from topic {message.topic}: {message.value}")
            self.process_message(message.topic, message.value)

    def process_message(self, topic, message):
        # Adicione a lógica de processamento da mensagem aqui
        print(f"Processing message from topic {topic}: {message}")

# Configuração do consumidor
bootstrap_servers = ['localhost:9092']
topics = ['iot', 'my-topic2']  # Lista de tópicos que você deseja consumir
group_id = 'my-group'

kafka_consumer = KafkaMessageConsumer(bootstrap_servers, topics, group_id)
