'''Configuración de URL para el proyecto de comercio electrónico.

La lista `urlpatterns` enruta las URL a las vistas. Para más información, consulte:
https://docs.djangoproject.com/en/5.2/topics/http/urls/
Ejemplos:
Vistas de función

1. Agregar una importación: `from my_app import views`

2. Agregar una URL a `urlpatterns`: `path('', views.home, name='home')
Vistas basadas en clases

1. Agregar una importación: `from other_app.views import Home`

2. Agregar una URL a `urlpatterns`: `path('', Home.as_view(), name='home')
Incluir otra URLconf

1. Importar la función `include()`: `from django.urls import include, path`

2. Agregar una URL a `urlpatterns`: `path('blog/', include('blog.urls'))
'''

# Importación de módulos necesarios
from django.contrib import admin  # Importa el módulo de administración de Django
from django.urls import path, include  # Importa la función path para definir rutas URL
from . import views  # Importa las vistas locales del directorio actual
from django.conf.urls.static import static  # Para servir archivos estáticos en desarrollo
from django.conf import settings  # Para acceder a las configuraciones del proyecto

# Definición de los patrones de URL
urlpatterns = [
    # Ruta para el panel de administración de Django
    # 'admin/' es la URL que mostrará el panel (ej: http://dominio.com/admin/)
    path('admin/', admin.site.urls),
    
    # Ruta principal (página de inicio)
    # '' representa la raíz del sitio (ej: http://dominio.com/)
    # views.home es la función que manejará esta ruta (definida en views.py)
    # name='home' le da un nombre único a esta URL para referenciarla en templates
    path('', views.home, name='home'),
    
    path('store/', include('store.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# La línea anterior solo funciona en modo DEBUG=True y sirve para:
# - Mostrar archivos multimedia (MEDIA_URL) durante el desarrollo
# - settings.MEDIA_ROOT indica dónde se almacenan físicamente los archivos
# - settings.MEDIA_URL es la URL base para acceder a estos archivos