from django.apps import AppConfig
from .kafka_consumer import kafka_consumer
import threading


class GraphsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphs'

    # def ready(self):
    #     # Inicia o consumidor em uma thread separada para não bloquear o servidor
    #     consumer_thread = threading.Thread(target=kafka_consumer.consume)
    #     consumer_thread.daemon = True
    #     consumer_thread.start()
