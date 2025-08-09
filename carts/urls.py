from django.urls import path, include
from . import views  # Importa las vistas locales del directorio actual

urlpatterns = [
    path('', views.cart, name='cart'),  # Ruta para ver el carrito
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),  # Ruta para ver el carrito
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
]