from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name= "store"),
    path('<slug:category_slug>',views.store, name='products_by_category'), # Creamos la url para filtrar por categoria <slug:category_slug> significa que es un slug y cambia el nombre de la categoria por un slug y el name hace referencia a la url
    path('<slug:category_slug>/<slug:product_slug>',views.product_detail, name='product_detail')
]