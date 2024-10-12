# Ensure Django uses the custom AppConfig
default_app_config = 'audit_logger.apps.AuditLoggerConfig'

# Import the AuditLogger class
from .logger import AuditLogger
