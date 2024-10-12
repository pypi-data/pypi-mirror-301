from django.apps import AppConfig, apps
from .helpers import *
from .logger import AuditLogger
from .kafka.main import KafkaProducer


class AuditLoggerConfig(AppConfig):
    name = 'audit_logger'

    def ready(self):
        bootstrap_servers = get_broker()
        producer_name = get_project_name()
        KafkaProducer.initialize(bootstrap_servers, producer_name)

        self.register_all_audit()
    def register_all_audit(self):
        """Registra los modelos definidos por el usuario y todos los modelos para auditoría."""

        # Cargar los modelos definidos en audit_config_models.py
        models_config_by_user = load_audit_config_models()

        # Registrar auditoría para modelos definidos por el usuario
        if models_config_by_user:
            for model in models_config_by_user:
                if table_exists(model._meta.db_table):
                    AuditLogger.register_auditoria_config(model)
                else:
                    print(f"Skipping AUDITORIA {model.__name__}, table does not exist.")

        # Registrar auditoría para todos los modelos en la aplicación
        all_models = apps.get_models()
        for model in all_models:
            if table_exists(model._meta.db_table):
                AuditLogger.register_auditoria_logs(model)
            else:
                print(f"Skipping AUDITORIA {model.__name__}, table does not exist.")

