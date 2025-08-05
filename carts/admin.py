from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

admin.site.register(Cart)  # Registra el modelo Cart en el panel de administración
admin.site.register(CartItem)  # Registra el modelo CartItem en el panel de administración