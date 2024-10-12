import json
import logging
from django.db import connection
from asgiref.sync import sync_to_async

class LocalAuditLogger:
    """Clase que maneja el registro de errores de Kafka en PostgreSQL sin migraciones."""

    def __init__(self):
        """Inicializa el auditor local y crea la tabla si no existe."""
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        """Crea la tabla kafka_local_logs si no existe en la base de datos."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS kafka_local_logs (
            id SERIAL PRIMARY KEY,
            error TEXT NOT NULL,
            registro JSONB NOT NULL,
            topic VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
                cursor.execute("SELECT to_regclass('public.kafka_local_logs')")
                table_exists = cursor.fetchone()
                if table_exists[0]:
                    logging.info("La tabla kafka_local_logs ya existía en la base de datos.")
                else:
                    logging.info("La tabla local kafka_local_logs fue creada exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear/verificar la tabla kafka_local_logs: {e}")

    @sync_to_async
    def local_log(self, topic, data, error_message):
        """Guarda el registro fallido en la base de datos PostgreSQL."""
        insert_query = '''
        INSERT INTO kafka_local_logs (error, registro, topic)
        VALUES (%s, %s, %s);
        '''
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_query, (error_message, json.dumps(data), topic))
                logging.info(f"Registro guardado localmente en PostgreSQL motivo: {error_message}")
            except Exception as db_error:
                logging.error(f"Error al guardar el mensaje en PostgreSQL: {db_error}")