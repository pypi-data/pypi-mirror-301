import threading
from django.utils.deprecation import MiddlewareMixin

# Variables de thread-local para almacenar la request y sus atributos
_thread_locals = threading.local()

def get_current_request():
    """
    Devuelve la request almacenada en el middleware.
    """
    return getattr(_thread_locals, 'request', None)

def set_current_request(request):
    """
        Modifica la request almacenada en el middleware.
    """
    return setattr(_thread_locals, 'request', request)

class AuditUserMiddleware(MiddlewareMixin):
    """
    Middleware combinado para capturar el usuario, la request, la URL, la IP y el dispositivo (user-agent).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener el usuario anterior desde la sesión
        previous_user = request.session.get('user_anterior', None)

        # Almacenar el usuario actual en thread-local antes de procesar la solicitud
        _thread_locals.previous_user = previous_user

        set_current_request(request)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user():
        """
        Devuelve el usuario actual de la solicitud.
        """
        request = get_current_request()
        user_id = getattr(request, 'user_id', None)
        if user_id:
            return user_id
        return None

    @staticmethod
    def get_previous_user():
        """
        Devuelve el usuario anterior almacenado en la sesión.
        """
        return getattr(_thread_locals, 'previous_user', None)

    @staticmethod
    def get_current_ip():
        """
        Devuelve la IP del cliente.
        """
        request = get_current_request()
        decoded_token = getattr(request, 'decoded_token', None)
        if decoded_token:
            datasession = decoded_token['dataUserSession']
            if datasession:
                ip = datasession['ip'] if datasession['ip'] else None
                return ip
            return None
        return None

    @staticmethod
    def get_user_agent():
        """
        Devuelve el User-Agent del cliente.
        """
        request = get_current_request()
        if request:
            return request.META.get('HTTP_USER_AGENT')
        return None

    @staticmethod
    def get_current_url():
        """
        Devuelve la URL completa de la solicitud actual.
        """
        request = get_current_request()
        if request:
            return request.path
        return None