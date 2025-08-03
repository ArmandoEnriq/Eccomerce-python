from django.db import models # Importamos el módulo models de Django para definir nuestros modelos
from django.urls import reverse  # Importamos reverse para generar URLs basadas en el slug de la categoría

# Create your models here.
class Category(models.Model): # Definimos la clase Category que hereda de models.Model(lo que nos permite crear un modelo de base de datos)
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta: # Clase Meta para definir opciones adicionales del modelo 
        verbose_name = 'category' # Nombre singular del modelo en el panel de administración
        verbose_name_plural = 'categories' # Nombre plural del modelo en el panel de administración
        
    def get_url(self): # Método para obtener la URL de la categoría
        return reverse('products_by_category', args=[self.slug]) # Utilizamos reverse para generar la URL basada en el slug de la categoría
    
    def __str__(self): # Método para representar el modelo como una cadena
        """Devuelve el nombre de la categoría como una cadena."""
        return self.category_name # Mostramos el nombre de la categoría como una cadena