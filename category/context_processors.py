from .models import Category

def menu_links(request): # Creamos un procesador de contexto que nos permite acceder a las categorias en cualquier plantilla
    links = Category.objects.all() # Obtenemos todas las categorias disponibles
    return dict(links=links) # Devolvemos un diccionario con las categorias que se pueden usar en las plantillas links es un nombre que se usará en las plantillas para acceder a las categorias