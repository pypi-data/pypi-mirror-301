import logging
import json
import os
import asyncio
from django.conf import settings
from confluent_kafka.admin import AdminClient
from aiokafka import AIOKafkaProducer

class KafkaProducer:
    _producer_name = None
    _aioproducer = None

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
            logging.error(f"El topic '{topic}' no existe.")
            raise Exception('ERROR EN KAFKA (TOPIC NO EXISTE)')

    @staticmethod
    async def _get_aioproducer():
        """Crea y configura el productor asíncrono de Kafka."""
        if KafkaProducer._aioproducer is None:
            KafkaProducer._producer_name = f"producer_{KafkaProducer._get_project_name()}"
            KafkaProducer._aioproducer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BROKER_URL,
                client_id=KafkaProducer._producer_name
            )
            await KafkaProducer._aioproducer.start()
        return KafkaProducer._aioproducer

    @staticmethod
    async def _send_event(topic, data):
        """Envía un evento a Kafka de manera asíncrona."""
        try:
            KafkaProducer._ensure_topic_exists(topic)

            producer = await KafkaProducer._get_aioproducer()

            if isinstance(data, dict):
                data['producer'] = KafkaProducer._producer_name
                data = json.dumps(data, ensure_ascii=False).encode('utf-8')  # Convierte el dict a JSON
            else:
                logging.error("El dato proporcionado no es un diccionario y no se puede serializar.")
                return

            # Envía el mensaje de forma asíncrona
            await producer.send_and_wait(topic, data)
            logging.info(f"Mensaje enviado correctamente a {topic}")

        except Exception as kafka_error:
            logging.error(f"Error al enviar mensaje a Kafka: {kafka_error}")

    @staticmethod
    def send_log_event(data):
        """Envía un evento de auditoría al topic de logs de manera asíncrona."""
        KafkaProducer._run_in_background(KafkaProducer._send_event, settings.KAFKA_TOPIC_LOGS, data)

    @staticmethod
    def send_error_event(data):
        """Envía un evento de error al topic de errores de manera asíncrona."""
        KafkaProducer._run_in_background(KafkaProducer._send_event, settings.KAFKA_TOPIC_ERRORS, data)

    @staticmethod
    def send_config_event(data):
        """Envía un evento de configuración al topic de configuración de manera asíncrona."""
        KafkaProducer._run_in_background(KafkaProducer._send_event, settings.KAFKA_TOPIC_CONFIG, data)

    @staticmethod
    def _run_in_background(coro, *args):
        """Ejecuta una tarea en segundo plano, sin bloquear el flujo principal."""
        try:
            # Intentar obtener el bucle de eventos actual
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # Si no hay un bucle de eventos en este thread, creamos uno
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Ejecuta la tarea en segundo plano sin bloquear
            if loop.is_running():
                asyncio.create_task(KafkaProducer._safe_run(coro, *args))
            else:
                # Si no hay un bucle de eventos corriendo, correr en un nuevo thread
                loop.run_in_executor(None, lambda: asyncio.run(KafkaProducer._safe_run(coro, *args)))

        except Exception as e:
            logging.error(f"Error ejecutando tarea asíncrona en segundo plano: {e}")

    @staticmethod
    async def _safe_run(coro, *args):
        """Envuelve una tarea asíncrona en un manejador de errores para que no bloquee."""
        try:
            await coro(*args)
        except Exception as e:
            logging.error(f"Error en la ejecución asíncrona: {e}")

    @staticmethod
    async def close_producer():
        """Cierra el productor de Kafka."""
        if KafkaProducer._aioproducer is not None:
            await KafkaProducer._aioproducer.stop()
            KafkaProducer._aioproducer = None

