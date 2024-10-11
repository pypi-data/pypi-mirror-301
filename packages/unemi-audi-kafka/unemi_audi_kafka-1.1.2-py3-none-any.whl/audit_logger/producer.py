import logging
from confluent_kafka import Producer
import json
import os
from django.conf import settings
from confluent_kafka.admin import AdminClient

class KafkaProducer:
    _producer_name = None

    @staticmethod
    def _get_project_name():
        """Obtiene el nombre del proyecto Django dinámicamente."""
        project_name = os.path.basename(settings.BASE_DIR)
        return project_name

    @staticmethod
    def _kafka_admin_client():
        """Crea un cliente administrativo de Kafka para operaciones sobre topics."""
        return AdminClient({'bootstrap.servers': settings.KAFKA_BROKER_URL})

    @staticmethod
    def _ensure_topic_exists(topic):
        """Verifica si el topic existe. Si no, lanza un error."""
        admin_client = KafkaProducer._kafka_admin_client()
        topic_metadata = admin_client.list_topics(timeout=10)

        if topic in topic_metadata.topics:
            logging.info(f"El topic '{topic}' ya existe.")
        else:
            # Lanza un error si el topic no existe
            logging.error(f"El topic '{topic}' no existe.")
            raise Exception('ERROR EN KAFKA (TOPIC NO EXISTE)')

    @staticmethod
    def _kafka_producer():
        """Crea y configura el productor de Kafka, incluyendo el nombre del productor."""
        if KafkaProducer._producer_name is None:
            KafkaProducer._producer_name = f"producer_{KafkaProducer._get_project_name()}"

        logging.info(f"Creando productor Kafka: {KafkaProducer._producer_name}")
        return Producer({
            'bootstrap.servers': settings.KAFKA_BROKER_URL,
            'client.id': KafkaProducer._producer_name  # Asigna un nombre al productor
        })

    @staticmethod
    def _send_event(topic, data):
        """Envía un evento a Kafka en el topic especificado como JSON."""
        # Verifica si el topic existe
        KafkaProducer._ensure_topic_exists(topic)

        producer = KafkaProducer._kafka_producer()

        if isinstance(data, dict):
            data['producer'] = KafkaProducer._producer_name
            data = json.dumps(data, ensure_ascii=False)  # Convierte el dict a JSON
        else:
            logging.error("El dato proporcionado no es un diccionario y no se puede serializar.")
            return

        # Envía el mensaje al topic correspondiente
        try:
            producer.produce(topic, value=data.encode('utf-8'))
            producer.flush()
            logging.info(f"Mensaje enviado correctamente al topic '{topic}'.")
        except Exception as e:
            logging.error(f"Error al enviar el mensaje al topic '{topic}': {e}")

    @staticmethod
    def send_log_event(data):
        """Envía un evento de auditoría al topic de logs."""
        KafkaProducer._send_event(settings.KAFKA_TOPIC_LOGS, data)

    @staticmethod
    def send_error_event(data):
        """Envía un evento de error al topic de errores."""
        KafkaProducer._send_event(settings.KAFKA_TOPIC_ERRORS, data)

    @staticmethod
    def send_config_event(data):
        """Envía un evento de configuración al topic de configuración."""
        KafkaProducer._send_event(settings.KAFKA_TOPIC_CONFIG, data)

