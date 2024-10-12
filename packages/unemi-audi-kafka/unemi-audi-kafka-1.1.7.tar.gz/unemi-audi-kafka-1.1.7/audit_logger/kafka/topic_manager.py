import logging
from confluent_kafka.admin import AdminClient

class KafkaTopicManager:
    def __init__(self, bootstrap_servers):
        """Inicializa KafkaTopicManager con un AdminClient que se reutiliza."""
        self.admin_client = AdminClient({'bootstrap.servers': bootstrap_servers, 'log_level': 4})
        logging.info(f"AdminClient inicializado correctamente en {bootstrap_servers}")

    def ensure_topic_exists(self, topic):
        """Verifica si el topic existe."""
        topic_metadata = self.admin_client.list_topics(timeout=10)

        if topic not in topic_metadata.topics:
            raise Exception(f'ERROR EN KAFKA (TOPIC NO EXISTE): {topic}')