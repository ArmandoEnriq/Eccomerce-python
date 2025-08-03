"""
ASGI config for ecommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# Configuración para servidores asíncronos (ej: Daphne, Uvicorn).
# Usado en aplicaciones que necesitan WebSockets o conexiones en tiempo real.

# Importa el módulo os para interactuar con el sistema operativo
# (especialmente con variables de entorno)
import os

# Importa la función get_asgi_application de Django que crea una aplicación ASGI (Asynchronous Server Gateway Interface).
from django.core.asgi import get_asgi_application

# Configura la variable de entorno DJANGO_SETTINGS_MODULE para que Django
# sepa qué configuración usar. En este caso, usa el módulo settings.py
# del proyecto ecommerce.
# Esto es esencial para que Django encuentre todas las configuraciones
# de tu proyecto (base de datos, aplicaciones instaladas, etc.)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Crea la aplicación ASGI que servirá como punto de entrada para
# servidores compatibles con ASGI (como Daphne, Uvicorn o Hypercorn)
# Esta variable 'application' es la que los servidores ASGI buscan por defecto
application = get_asgi_application()