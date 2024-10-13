import logging
import asyncio

from .topic_manager import KafkaTopicManager
from .async_producer import KafkaAsyncProducer
from .local_logger import LocalAuditLogger

class KafkaProducer:
    _log_topic = 'audit_logs'
    _error_topic = 'audit_errors'
    _config_topic = 'audit_config'
    _producer = None
    _topic_manager = None
    _local_logger = None

    @classmethod
    def initialize(cls, bootstrap_servers, producer_name):
        """Inicializa los atributos de clase con los valores de configuración."""
        cls._producer = KafkaAsyncProducer(bootstrap_servers, producer_name)
        cls._topic_manager = KafkaTopicManager(bootstrap_servers)
        cls._local_logger = LocalAuditLogger()

    @classmethod
    async def _send_event(cls, topic, data):
        """Envía un evento a Kafka utilizando el productor asíncrono."""
        try:
            cls._topic_manager.ensure_topic_exists(topic)
            await cls._producer.send_event(topic, data)
        except Exception as kafka_error:
            logging.warning(f"Error al enviar mensaje a Kafka: {kafka_error}")
            await cls._local_logger.local_log(topic, data, str(kafka_error))

    @staticmethod
    def send_log_event(data):
        """Envía un evento de auditoría al topic de logs de manera asíncrona."""
        KafkaProducer._run_in_background(KafkaProducer._send_event, KafkaProducer._log_topic, data)

    @staticmethod
    def send_error_event(data):
        """Envía un evento de error al topic de errores de manera asíncrona."""
        KafkaProducer._run_in_background(KafkaProducer._send_event, KafkaProducer._error_topic, data)

    @staticmethod
    def send_config_event(data):
        """Envía un evento de configuración al topic de configuración de manera asíncrona."""
        KafkaProducer._run_in_background(KafkaProducer._send_event, KafkaProducer._config_topic, data)

    @staticmethod
    def _run_in_background(coro, *args):
        """Ejecuta una tarea en segundo plano, sin bloquear el flujo principal."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            asyncio.create_task(KafkaProducer._safe_run(coro, *args))
        else:
            loop.run_in_executor(None, lambda: asyncio.run(KafkaProducer._safe_run(coro, *args)))

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





