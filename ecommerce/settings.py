from pathlib import Path

# Configuración de rutas base del proyecto
#Aqui se encuentra el corazon del proyecto  Contiene toda la configuración (BD, apps, middlewares, templates, etc.).

# BASE_DIR representa el directorio principal del proyecto (donde está manage.py)
# Se usa Path de pathlib para manejo de rutas multiplataforma
BASE_DIR = Path(__file__).resolve().parent.parent # Usamos la ruta actual y la transformamos en absoluta por ejemplo, convierte /foo/../bar en /bar) y con parent subimos una carpeta en este caso 2 para llegar a manage.py


# Configuración rápida para desarrollo - NO adecuada para producción
# Ver https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡Mantener secreta la clave secreta en producción!
# Esta clave se usa para cifrado y debe ser única y secreta en entornos reales
SECRET_KEY = 'django-insecure-)i$jgw#f%no-uz0j(($*+6)5&i574ni#tl$imn)insm+b@z^u9'

# ADVERTENCIA DE SEGURIDAD: ¡No activar DEBUG en producción!
# DEBUG=True muestra errores detallados, útil en desarrollo pero peligroso en producción
DEBUG = True

# Hosts/dominios permitidos para el sitio (vacío permite todos en DEBUG=True)
# En producción debe contener los dominios reales del sitio
ALLOWED_HOSTS = []


# Definición de aplicaciones instaladas
# Aquí se registran todas las apps Django y apps de terceros que usa el proyecto
INSTALLED_APPS = [
    'django.contrib.admin',       # Interfaz de administración
    'django.contrib.auth',        # Sistema de autenticación
    'django.contrib.contenttypes',# Framework de tipos de contenido
    'django.contrib.sessions',    # Manejo de sesiones
    'django.contrib.messages',    # Sistema de mensajes
    'django.contrib.staticfiles', # Manejo de archivos estáticos
    
    # Apps personalizadas del proyecto
    'category',  # App para manejar categorías de productos
    'accounts',  # App para manejo de usuarios y autenticación
    'store',     # App principal para la tienda/comercio electrónico
]

# Middleware - componentes que procesan requests/responses globalmente
# El orden es importante ya que se ejecutan de arriba hacia abajo
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Seguridad básica
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manejo de sesiones
    'django.middleware.common.CommonMiddleware',      # Procesamiento común
    'django.middleware.csrf.CsrfViewMiddleware',      # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware',     # Mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Protección clickjacking
]

# Configuración de URLs principales del proyecto
ROOT_URLCONF = 'ecommerce.urls'

# Configuración de plantillas (templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de templates
        'DIRS': ['templates'],  # Directorios donde buscar templates (además de los de cada app)
        'APP_DIRS': True,       # Buscar templates en subdirectorio 'templates' de cada app
        'OPTIONS': {
            'context_processors': [  # Procesadores de contexto que añaden variables a los templates
                'django.template.context_processors.request',      # Añade el objeto 'request'
                'django.contrib.auth.context_processors.auth',     # Info de autenticación
                'django.contrib.messages.context_processors.messages',  # Sistema de mensajes
                'category.context_processors.menu_links',  # Procesador de contexto personalizado para categorías
            ],
        },
    },
]

# Configuración WSGI para despliegue en producción
#Web Server Gateway Interface es un estándar de Python que define cómo los servidores web se comunican con aplicaciones web
WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Modelo de usuario personalizado (sobrescribe el modelo por defecto de Django)
AUTH_USER_MODEL = 'accounts.Account'  # Usa el modelo Account definido en la app accounts


# Configuración de base de datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Por defecto usa SQLite, pero puede cambiarse a PostgreSQL, MySQL, etc.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Motor de base de datos
        'NAME': BASE_DIR / 'db.sqlite3',         # Ruta al archivo de la base de datos
    }
}


# Validación de contraseñas
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
# Estas configuraciones definen requisitos de fortaleza para las contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Evita contraseñas similares a información del usuario
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Longitud mínima
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Evita contraseñas comunes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Evita contraseñas solo numéricas
    },
]


# Configuración de internacionalización
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'en-us'  # Idioma por defecto (inglés)
TIME_ZONE = 'UTC'        # Zona horaria (UTC por defecto)
USE_I18N = True         # Habilitar internacionalización
USE_TZ = True           # Usar zonas horarias


# Configuración de archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = 'static/'  # URL base para archivos estáticos (ej. /static/css/style.css)  Define la URL base para acceder a archivos estáticos en desarrollo
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directorio donde se recolectarán TODOS los archivos estáticos para producción
STATICFILES_DIRS = [    # Lista de directorios adicionales donde Django buscará archivos estáticos Solo relevante cuando ejecutas collectstatic
                    #python manage.py collectstatic  # Copia todos los estáticos a STATIC_ROOT
    'ecommerce/static'  # Directorio static en la raíz del proyecto
]

# Configuración de archivos multimedia (subidos por usuarios)
MEDIA_URL = '/media/'  # URL base para acceder a archivos subidos por usuarios
MEDIA_ROOT = BASE_DIR / 'media'  # Ruta en el sistema de archivos donde se guardan los archivos subidos

# Tipo de campo automático por defecto para modelos
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Usa campos AutoField grandes (64 bits)