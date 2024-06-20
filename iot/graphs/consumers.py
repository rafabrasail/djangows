import json
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class KafkaMessageConsumer:
    def __init__(self, bootstrap_servers, group_id):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id

    def consume(self, topics):
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        channel_layer = get_channel_layer()
        for message in consumer:
            async_to_sync(channel_layer.group_send)(
                "kafka_group",
                {
                    "type": "kafka.message",
                    "message": message.value,
                },
            )

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("kafka_group", self.channel_name)
        await self.accept()

        # Inicia o consumidor Kafka em uma thread separada
        topics = ['iot', 'my-topic2']  # Lista de tópicos que você deseja consumir
        thread = threading.Thread(target=self.start_kafka_consumer, args=(topics,))
        thread.daemon = True
        thread.start()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("kafka_group", self.channel_name)

    async def receive(self, text_data):
        pass

    def start_kafka_consumer(self, topics):
        kafka_consumer = KafkaMessageConsumer(
            bootstrap_servers=['localhost:9092'],
            group_id='my-group'
        )
        kafka_consumer.consume(topics)

    async def kafka_message(self, event):
        message = event['message']

        # Envia a mensagem para o WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
