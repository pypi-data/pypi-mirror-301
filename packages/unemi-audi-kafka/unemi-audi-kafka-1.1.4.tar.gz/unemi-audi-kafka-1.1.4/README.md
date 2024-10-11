# Unemi Audit Kafka

`unemi-audi-kafka` es una aplicacion reutilizable de Django que audita automaticamente los cambios en los modelos (creacion, actualizacion, eliminacion) en todos los modelos de tu proyecto Django. Se integra con Kafka para el envio de logs y permite una auditoria configurable para los modelos importantes. La aplicacion captura metadatos utiles como el usuario que realizo los cambios, la IP de la solicitud, la URL y mas.

## Caracteristicas

- **Auditoria Automatica**: Registra automaticamente todos los modelos de Django para el registro de auditoria.
- **Integracion con Kafka**: Utiliza `confluent_kafka` para enviar los registros de auditoria a los temas de Kafka.
- **Auditoria de Configuracion**: Registra manualmente modelos importantes para la auditoria de configuracion.
- **Middleware de Contexto de Usuario**: Captura informacion sobre el usuario, la IP de la solicitud y el agente de usuario a traves de middleware.
- **Personalizable**: Puedes extender o sobrescribir middleware, y controlar el comportamiento del productor de Kafka.

## Instalacion

1. **INSTALAR la libreria usando pip**:

   ```bash
   pip install unemi-audi-kafka

   ```

2. **Agregar la libreria en Django INSTALLED_APPS**:

   En tu `settings.py`, configura las aplicaciones:

   ```python
   INSTALLED_APPS = [
      # Other installed apps
      'audit_logger',
   ]

   ```

3. **Agregar el MIDDLEWARE**:

   En tu `settings.py`, configura las middlewares:

   ```python
   MIDDLEWARE = [
      # Other middlewares
      'audit_logger.middlewares.AuditUserMiddleware',
   ]

   ```

4. **Agregar CONFIGURACIONES DE KAFKA**:

   En tu `settings.py`, configurar los Kafka broker y topics:

   ```python
   KAFKA_BROKER_URL = '35.212.2.202:9092'  # Replace with your Kafka broker URL
   KAFKA_TOPIC_LOGS = 'audit_logs'      # Topic for log auditing
   KAFKA_TOPIC_ERRORS = 'audit_errors'  # Topic for error logging
   KAFKA_TOPIC_CONFIG = 'audit_config'  # Topic for configuration auditing

   ```

5. **Agregar REQUEST en el LOGIN**:

   En tu `decorators_helper.py`, agregar en la funcion de login_required:

   ```python
   from audit_logger.middlewares import set_current_request

   def login_required(f):
      def new_f(view, request):
        # code for decoded token
        set_current_request(request)
        return f(view, request)
   ```

## Opcional auditar tablas de configuracion

Si deseas guardar las configuraciones de tu aplicacion, la puedes separar de los otras tablas con:

En tu `models.py`, agregar modelo manualmente:

```python
    from audit_logger import AuditLogger

    class Configuracion(ModelBase):
    nombre = models.CharField(unique=True, max_length=100, verbose_name=u'Nombre')

    # Registrar Configuracion
    AuditLogger.register_auditoria_config(Configuracion)
```

O también podrías auditarlos en un archivo aparte para saber que modelos se encuentran allí.
crear un archivo audit_config_models.py ubicado en la misma carpeta donde se encuentra el archivo settings.py

```python
   # audit_config_models.py

    # Importa los modelos que deseas auditar
    from myapp.models import MyModel1, MyModel2
    from anotherapp.models import AnotherModel

    # Define una lista con los modelos que quieres auditar
    CONFIG_MODELS = [
    MyModel1,  # Modelo 1 de la aplicación myapp
    MyModel2,  # Modelo 2 de la aplicación myapp
    AnotherModel,  # Modelo de otra aplicación
    ]

```

## Opcional auditar tablas de manejo de errores

Si deseas auditar errores críticos en algún punto del código, lo puedes hacer con la excepción dentro de un catch.

```python
   from audit_logger import AuditLogger

    try:
        # CODIGO RIESGOSO
    except Exception as ex:
        AuditLogger.register_auditoria_errors(ex)

```
