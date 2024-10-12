from aiokafka import AIOKafkaProducer
import logging
import json

class KafkaAsyncProducer:
    """Clase que maneja el productor asíncrono de Kafka."""
    def __init__(self, bootstrap_servers, producer_name):
        self._bootstrap_servers = bootstrap_servers
        self._producer_name = producer_name
        self._aioproducer = None

    async def _get_aioproducer(self):
        """Crea y configura el productor asíncrono de Kafka si no está inicializado."""
        if self._aioproducer is None:
            try:
                self._aioproducer = AIOKafkaProducer(
                    bootstrap_servers=self._bootstrap_servers,
                    client_id=self._producer_name
                )
                await self._aioproducer.start()
            except Exception as e:
                logging.error(f"Error al conectar con Kafka: {e}")
                raise
        return self._aioproducer

    async def send_event(self, topic, data):
        """Envía un evento a Kafka de manera asíncrona."""
        producer = await self._get_aioproducer()

        if isinstance(data, dict):
            data['producer'] = self._producer_name
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')  # Convierte el dict a JSON
        else:
            logging.error("El dato proporcionado no es un diccionario y no se puede serializar.")
            return

        try:
            await producer.send_and_wait(topic, data)
            logging.info(f"Mensaje enviado correctamente a {topic}")
        except Exception as kafka_error:
            logging.error(f"Error al enviar mensaje a Kafka: {kafka_error}")
            raise

    async def close(self):
        """Cierra el productor de Kafka."""
        if self._aioproducer is not None:
            await self._aioproducer.stop()
            self._aioproducer = None