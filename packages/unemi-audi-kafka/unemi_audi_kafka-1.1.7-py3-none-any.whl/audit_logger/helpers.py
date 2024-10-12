from django.conf import settings
from django.db import connection
import importlib.util
import os

def get_project_name():
    """Obtiene el nombre del proyecto Django dinámicamente."""
    project_name = os.path.basename(settings.BASE_DIR)
    return project_name

def get_broker():
    return getattr(settings, 'KAFKA_BROKER_URL', 'localhost:9092')

def table_exists(table_name):
    """Verifica si la tabla existe en la base de datos."""
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT 1 FROM information_schema.tables WHERE table_name = %s", [table_name])
        return cursor.fetchone() is not None

def get_settings_module_path():
    """Obtén la ruta donde se encuentra settings.py, usando el módulo de configuración."""
    from django.conf import settings

    # Obtener el módulo de configuración (settings.py) usando importlib
    settings_module = settings.SETTINGS_MODULE
    spec = importlib.util.find_spec(settings_module)

    if spec is None:
        raise RuntimeError(f"No se pudo encontrar el módulo {settings_module}")

    # Devolver la ruta del directorio que contiene settings.py
    return os.path.dirname(spec.origin)

def get_project_root(settings_module_path):
    """Obtén la ruta raíz del proyecto (un nivel por encima de settings_module_path)."""
    return os.path.dirname(settings_module_path)

def load_audit_config_models():
    """Carga los modelos definidos en audit_config_models.py."""
    try:
        # Obtener la ruta donde se encuentra settings.py
        settings_module_path = get_settings_module_path()

        # Primero buscar en la misma carpeta que settings.py
        audit_logger_path = os.path.join(settings_module_path, 'audit_config_models.py')

        # Si no se encuentra, probar un nivel por encima de settings_module_path
        if not os.path.exists(audit_logger_path):
            root_dir = get_project_root(settings_module_path)
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