from django.db import models
from category.models import Category
from django.urls import reverse # Importamos reverse para generar URLs basadas en nombres de vistas

# Create your models here.
class Product(models.Model): # Definimos la clase Product que hereda de models.Model (lo que nos permite crear un modelo de base de datos)
    """Modelo para representar un producto en la tienda."""
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):  # Método para obtener la URL del producto
        """Devuelve la URL del producto."""
        return reverse('product_detail', args=[self.category.slug, self.slug]) # Utilizamos reverse para generar la URL basada en el nombre de la vista 'product_detail' y pasamos los argumentos necesarios (slug de la categoría y slug del producto)

    def __str__(self):
        return self.product_name
    
    
class VariationManager(models.Manager): # Creamos un manager personalizado para la clase Variation
    def colors(self): # Método para obtener las variaciones de color
        return super(VariationManager, self).filter(variation_category='color', is_active=True) # Devuelve las variaciones de color activas
    def tallas(self): # Método para obtener las variaciones de talla
        return super(VariationManager, self).filter(variation_category='talla', is_active=True) # Devuelve las variaciones de talla activas

    
class Variation(models.Model): # Creamos la clase variations para representar las variaciones de un producto
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # creamos una llave foranea a la clase Product
    variation_category = models.CharField(max_length=100, choices=(
        ('color', 'color'),
        ('talla', 'talla'),
    )) # Creamos un campo para la categoría de la variación
    variation_value = models.CharField(max_length=100) # Creamos un campo para el valor de la variación
    is_active = models.BooleanField(default=True) # Creamos un campo para indicar si la variación es activa
    created_date = models.DateTimeField(auto_now_add=True) # Creamos un campo para la fecha de creación
    
    objects = VariationManager()

    def __unicode__(self):
        return self.product  # Retorna el nombre del producto como representación de la variación