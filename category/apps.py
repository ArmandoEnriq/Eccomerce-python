from django.apps import AppConfig # Importamos AppConfig para configurar nuestra aplicación Django


class CategoryConfig(AppConfig): # Clase de configuración para la aplicación Category usamos AppConfig para definir la configuración de la aplicación
    default_auto_field = 'django.db.models.BigAutoField' # Con default_auto_field especificamos el tipo de campo para los identificadores automáticos el cual usara BigAutoField que sirve de identificador único para los modelos de grande escala
    name = 'category' # Nombre de la aplicación, debe coincidir con el nombre del directorio de la aplicación
