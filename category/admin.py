from django.contrib import admin # Importamos el módulo de administración de Django
from .models import Category # Importamos nuestro modelo Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin): # Clase para personalizar la administración del modelo Category usamos admin.ModelAdmin para personalizar la vista en el panel de administración
    prepopulated_fields = {'slug': ('category_name',)}  # prepopulated_fields sirve para Automaticamente llenar el campo slug basado en category_name
    list_display = ('category_name', 'slug')  # Campos que se mostrarán en la lista de categorías


admin.site.register(Category, CategoryAdmin) # Registramos el modelo Category con su configuración personalizada del panel de administración