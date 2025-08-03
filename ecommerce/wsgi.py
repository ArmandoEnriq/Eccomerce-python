"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

#(Web Server Gateway Interface)
# Punto de entrada para servidores tradicionales (ej: Gunicorn, Apache, Nginx).
# Usado en despliegues en producción.

# Importación del módulo os para interactuar con el sistema operativo
import os

# Importación de la función get_wsgi_application de Django
# WSGI = Web Server Gateway Interface (Interfaz de Pasarela para Servidores Web)
from django.core.wsgi import get_wsgi_application

# Configuración de la variable de entorno DJANGO_SETTINGS_MODULE
# Esto le indica a Django qué archivo de configuración usar (en este caso, ecommerce/settings.py)
# 'ecommerce.settings' sigue la notación Python de rutas de módulos:
# - ecommerce = nombre del paquete/proyecto
# - settings = nombre del módulo (settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Obtención de la aplicación WSGI
# Esta es la variable que los servidores web (como Apache, Nginx o Gunicorn) buscarán
# y usarán para servir la aplicación Django
application = get_wsgi_application()