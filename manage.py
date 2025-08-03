#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Utilidad de línea de comandos de Django para tareas administrativas.
"""

import os
import sys


def main():
    """Función principal que ejecuta tareas administrativas."""
    # Configura la variable de entorno DJANGO_SETTINGS_MODULE para que Django
    # sepa qué configuración usar (en este caso, ecommerce.settings)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    try:
        # Intenta importar la función execute_from_command_line de Django
        # que es el núcleo del sistema de manejo de comandos
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado o no se puede importar, muestra este error
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Ejecuta el comando recibido desde la línea de comandos
    # sys.argv contiene los argumentos pasados al script
    # Ejemplo: ['manage.py', 'runserver', '8000']
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Punto de entrada cuando el script se ejecuta directamente
    # (no cuando se importa como módulo)
    main()