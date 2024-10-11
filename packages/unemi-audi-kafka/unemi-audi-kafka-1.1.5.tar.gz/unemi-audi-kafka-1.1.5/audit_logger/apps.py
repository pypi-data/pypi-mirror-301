import importlib.util
import os
from django.apps import AppConfig, apps
from django.db import connection
from .logger import AuditLogger


class AuditLoggerConfig(AppConfig):
    name = 'audit_logger'

    def ready(self):
        # Registrar automáticamente todos los modelos para auditoría
        self.register_all_audit()

    def register_all_audit(self):
        """Registra los modelos definidos por el usuario y todos los modelos para auditoría."""

        # Cargar los modelos definidos en audit_config_models.py
        models_config_by_user = self.load_audit_config_models()

        # Registrar auditoría para modelos definidos por el usuario
        if models_config_by_user:
            for model in models_config_by_user:
                if self.table_exists(model._meta.db_table):
                    AuditLogger.register_auditoria_config(model)
                else:
                    print(f"Skipping AUDITORIA {model.__name__}, table does not exist.")

        # Registrar auditoría para todos los modelos en la aplicación
        all_models = apps.get_models()
        for model in all_models:
            if self.table_exists(model._meta.db_table):
                AuditLogger.register_auditoria_logs(model)
            else:
                print(f"Skipping AUDITORIA {model.__name__}, table does not exist.")

    def load_audit_config_models(self):
        """Carga los modelos definidos en audit_config_models.py."""
        try:
            # Obtener la ruta donde se encuentra settings.py
            settings_module_path = self.get_settings_module_path()

            # Primero buscar en la misma carpeta que settings.py
            audit_logger_path = os.path.join(settings_module_path, 'audit_config_models.py')

            # Si no se encuentra, probar un nivel por encima de settings_module_path
            if not os.path.exists(audit_logger_path):
                root_dir = self.get_project_root(settings_module_path)
                audit_logger_path = os.path.join(root_dir, 'audit_config_models.py')

            # Verificar si el archivo existe
            if not os.path.exists(audit_logger_path):
                raise FileNotFoundError(f"{audit_logger_path} not found.")

            # Cargar dinámicamente el archivo audit_config_models.py
            spec = importlib.util.spec_from_file_location("audit_config_models", audit_logger_path)
            audit_config_models = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(audit_config_models)

            # Devolver la lista de modelos definidos por el usuario
            return getattr(audit_config_models, 'CONFIG_MODELS', [])
        except (FileNotFoundError, AttributeError) as e:
            print(f"Error: {e}")
            return []

    def get_settings_module_path(self):
        """Obtén la ruta donde se encuentra settings.py, usando el módulo de configuración."""
        from django.conf import settings

        # Obtener el módulo de configuración (settings.py) usando importlib
        settings_module = settings.SETTINGS_MODULE
        spec = importlib.util.find_spec(settings_module)

        if spec is None:
            raise RuntimeError(f"No se pudo encontrar el módulo {settings_module}")

        # Devolver la ruta del directorio que contiene settings.py
        return os.path.dirname(spec.origin)

    def get_project_root(self, settings_module_path):
        """Obtén la ruta raíz del proyecto (un nivel por encima de settings_module_path)."""
        return os.path.dirname(settings_module_path)

    def table_exists(self, table_name):
        """Verifica si la tabla existe en la base de datos."""
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM information_schema.tables WHERE table_name = %s", [table_name])
            return cursor.fetchone() is not None

