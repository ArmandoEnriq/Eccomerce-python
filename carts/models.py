from django.db import models
from store.models import Product, Variation
# Create your models here.

class Cart(models.Model):
    """
    Modelo para representar un carrito de compras.
    Cada carrito puede contener múltiples productos.
    """
    cart_id = models.CharField(max_length=255, blank=True)  # Identificador único del carrito
    date_added = models.DateField(auto_now_add=True)  # Fecha en que se creó el carrito

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    """
    Modelo para representar un producto dentro de un carrito de compras.
    Cada CartItem está asociado a un Cart y a un Product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Producto asociado
    variations= models.ManyToManyField(Variation, blank=True) # Crea una relacion muchos a muchos con la tabla Variation
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Carrito al que pertenece
    quantity = models.IntegerField()  # Cantidad del producto en el carrito
    is_active = models.BooleanField(default=True)  # Indica si el item está activo

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product  # Retorna el nombre del producto como representación del CartItem 