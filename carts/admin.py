from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)  # Registra el modelo Cart en el panel de administración
admin.site.register(CartItem, CartItemAdmin)  # Registra el modelo CartItem en el panel de administración