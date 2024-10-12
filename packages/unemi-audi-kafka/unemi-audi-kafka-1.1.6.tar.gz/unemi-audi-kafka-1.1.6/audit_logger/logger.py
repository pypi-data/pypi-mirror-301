import copy
import sys
import traceback
import inspect
from decimal import Decimal
from django.core.files import File
from datetime import date as DateClass, datetime as DateTimeClass, time
from django.db.models.signals import pre_save, post_save, post_delete
from django.forms.models import model_to_dict

from .middlewares import AuditUserMiddleware
from kafka.main import KafkaProducer

class AuditLogger:
    previous_instance_state = {}
    registered_models_logs = set()  # Track models registered for log auditing
    registered_models_config = set()  # Track models registered for config auditing

    @staticmethod
    def register_auditoria_logs(model):
        """Registers a model for log auditing."""
        if model in AuditLogger.registered_models_config:
            print(f"Skipping {model.__name__} for logs as it's already registered for config.")
            return

        if model not in AuditLogger.registered_models_logs:
            AuditLogger._register_auditoria(model, 'logs')
            AuditLogger.registered_models_logs.add(model)
            print(f"Registered {model.__name__} for log auditing.")

    @staticmethod
    def register_auditoria_config(model):
        """Registers a model for configuration auditing."""
        # Unbind log auditing if it's already registered
        if model in AuditLogger.registered_models_logs:
            AuditLogger._unregister_auditoria_logs(model)
            print(f"Unregistered {model.__name__} from log auditing for config registration.")

        if model not in AuditLogger.registered_models_config:
            AuditLogger._register_auditoria(model, 'config')
            AuditLogger.registered_models_config.add(model)
            print(f"Registered {model.__name__} for configuration auditing.")

    @staticmethod
    def _unregister_auditoria_logs(model):
        """Unregisters a model from log auditing."""
        pre_save.disconnect(AuditLogger._audit_pre_save, sender=model)
        post_save.disconnect(sender=model)
        post_delete.disconnect(sender=model)
        AuditLogger.registered_models_logs.discard(model)
        print(f"Model {model.__name__} unregistered from log auditing.")

    @staticmethod
    def register_auditoria_errors(exception):
        """Captures system errors for auditing."""
        AuditLogger._audit_error(exception)

    @staticmethod
    def _register_auditoria(model, event_type):
        """General method to register models for auditing."""
        pre_save.connect(AuditLogger._audit_pre_save, sender=model)
        post_save.connect(
            lambda sender, instance, created, **kwargs: AuditLogger._audit_post_save(sender, instance, created, event_type),
            sender=model, weak=False
        )
        post_delete.connect(
            lambda sender, instance, **kwargs: AuditLogger._audit_post_delete(sender, instance, event_type),
            sender=model, weak=False
        )

    @staticmethod
    def _audit_pre_save(sender, instance, **kwargs):
        """Captures the previous state before changes are saved."""
        if instance.pk:
            try:
                previous_instance = sender.objects.get(pk=instance.pk)
                AuditLogger.previous_instance_state[instance.pk] = copy.deepcopy(previous_instance)
            except sender.DoesNotExist:
                pass

    @staticmethod
    def _audit_post_save(sender, instance, created, event_type, **kwargs):
        """Audits actions after a model is saved."""
        current_user, previous_user, context_info = AuditLogger._get_user_context(sender, instance)
        previous_instance = AuditLogger.previous_instance_state.get(instance.pk)

        previous_state = AuditLogger._serialize_instance(previous_instance) if previous_instance else None
        current_state = AuditLogger._serialize_instance(instance)
        action = 'created' if created else 'updated'

        # Handle logical deletion
        if not created and previous_state and current_state.get('es_activo') == False and previous_state.get('es_activo') == True:
            action = 'logic_deleted'

        audit_data = AuditLogger._build_audit_data(
            instance, sender, action, current_user, previous_user, previous_state, current_state, **context_info
        )

        AuditLogger._send_event(event_type, audit_data)
        AuditLogger.previous_instance_state.pop(instance.pk, None)

    @staticmethod
    def _audit_post_delete(sender, instance, event_type, **kwargs):
        """Audits actions after a model is deleted."""
        current_user, previous_user, context_info = AuditLogger._get_user_context(sender, instance)
        previous_state = AuditLogger._serialize_instance(instance) if instance else None

        audit_data = AuditLogger._build_audit_data(
            instance, sender, 'deleted', current_user, previous_user, previous_state, None, **context_info
        )

        AuditLogger._send_event(event_type, audit_data)

    @staticmethod
    def _audit_error(exception):
        """Handles error auditing."""
        exc_type, _, exc_tb = sys.exc_info()
        error_type = exc_type.__name__
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        current_user, _, context_info = AuditLogger._get_user_context()

        audit_data = {
            "error_type": error_type,
            "error_message": str(exception),
            "stack_trace": traceback.format_exc(),
            "file_name": file_name,
            "line_number": line_number,
            "timestamp": str(DateTimeClass.now()),
            "current_user": current_user or 'Anonymous',
            **context_info
        }

        KafkaProducer.send_error_event(audit_data)

    @staticmethod
    def _build_audit_data(instance, sender, action, current_user, previous_user, previous_state, current_state, **context):
        """Builds the audit data dictionary."""
        frame = inspect.stack()[2]
        event_file = frame.filename
        event_line = frame.lineno

        return {
            "model": sender.__name__,
            "instance_id": getattr(instance, 'id', None),
            "description": getattr(instance, 'auditoria_descripcion', None),
            "action": action,
            "current_user": current_user or None,
            "previous_user": previous_user or None,
            "module": sender.__module__,
            "previous_state": previous_state,
            "current_state": current_state,
            "timestamp": str(DateTimeClass.now()),
            "event_file": event_file,
            "event_line": event_line,
            **context
        }

    @staticmethod
    def _get_user_context(sender=None, instance=None):
        """Gets the current user, previous user, and other contextual info."""
        current_user = AuditUserMiddleware.get_current_user()
        previous_user = AuditUserMiddleware.get_previous_user()
        context = {
            "url": AuditUserMiddleware.get_current_url(),
            "ip_address": AuditUserMiddleware.get_current_ip(),
            "user_agent": AuditUserMiddleware.get_user_agent(),
        }

        return current_user, previous_user, context

    @staticmethod
    def _send_event(event_type, audit_data):
        """Sends the appropriate event to Kafka."""
        if event_type == 'logs':
            KafkaProducer.send_log_event(audit_data)
        elif event_type == 'config':
            KafkaProducer.send_config_event(audit_data)

    @staticmethod
    def _serialize_instance(instance):
        """Converts a model instance to a serializable dictionary, including ManyToMany fields."""
        # Convertir los campos regulares con model_to_dict
        data = model_to_dict(instance, exclude=[field.name for field in instance._meta.many_to_many])

        # Serializar campos ManyToMany
        for field in instance._meta.many_to_many:
            value = getattr(instance, field.name)
            data[field.name] = list(value.values_list('id', flat=True))  # Solo los IDs de los objetos relacionados

        # Procesar otros tipos de campos
        for field in instance._meta.fields:
            value = getattr(instance, field.name)

            if isinstance(value, File):
                data[field.name] = value.url if value else None
            elif isinstance(value, Decimal):
                data[field.name] = float(value)
            elif isinstance(value, (DateClass, DateTimeClass)):
                data[field.name] = value.isoformat()
            elif isinstance(value, time):
                data[field.name] = value.strftime('%H:%M:%S')

        return data