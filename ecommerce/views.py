# Importa la función render para procesar templates y devolver respuestas HTTP
from django.shortcuts import render
from store.models import Product  # Importa el modelo Product para acceder a los productos de la tienda

# Definición de la vista para la página de inicio
def home(request): # Vista principal que renderiza la página de inicio.
    """ Parámetros:
        request (HttpRequest): Objeto que contiene metadatos sobre la solicitud,
                               como método HTTP, parámetros, usuario, etc.
        Retorna:
        HttpResponse: Respuesta que incluye el template renderizado."""
    products = Product.objects.all().filter(is_available=True) # Obtiene todos los productos si están disponibles
    
    context = {
        'products': products,  # Pasa los productos disponibles al contexto del template
    }

    # La función render combina un template con un contexto (opcional) y
    # devuelve un objeto HttpResponse
    return render(request, 'home.html', context)
    # Argumentos:
    # 1. request: Contirnr la informacion de peticion User, POST GET y se inyecta en el archivo html que vamos a devolver 
    # 2. 'home.html': Ruta del template a renderizar devuelve el archivo html
    # 3. (Opcional) context: Diccionario con datos para pasar al template