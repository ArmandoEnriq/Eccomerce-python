from django.contrib import admin
from .models import Product, Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin): # Clase para personalizar la administración del modelo Product y usamos admin.ModelAdmin para personalizar la vista en el panel de administración
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available', 'modified_date')# Campos que se mostrarán en la lista de productos en el panel de administración
    prepopulated_fields = {'slug': ('product_name',)} # prepopulated_fields sirve para Automaticamente llenar el campo slug basado en product_name
    list_filter = ('category', 'is_available') # Campos que se usarán para filtrar los productos en el panel de administración
    search_fields = ('product_name', 'description') # Campos que se usarán para buscar productos en el panel de administración
    ordering = ('-created_date',) # Ordenamiento por defecto (los más recientes primero)
    
class VarationAdmin(admin.ModelAdmin): # Clase para personalizar la administración del modelo Varation y usamos admin.ModelAdmin para personalizar la vista en el panel de administración
    list_display = ('product', 'variation_category', 'variation_value', 'is_active') # Campos que se mostrarán en la lista de variaciones en el panel de administración
    list_editable = ('is_active',) # Campos que se puedan editar en la lista de variaciones en el panel de administración
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active') # Campos que se usarán para filtrar las variaciones en el panel de administración

admin.site.register(Product, ProductAdmin) # Registramos el modelo Product con su configuración personalizada del panel de administración
admin.site.register(Variation, VarationAdmin) # Registramos el modelo Varation en el panel de administración