# Logica de la vista 

from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None): # Creamos la vista de la tienda, category_slug es un parametro opcional que nos permite filtrar por categoria
    categories = None # Obtenemos las categorias, inicialmente es None
    products = None # Obtenemos los productos, inicialmente es None

    if category_slug is not None: # Si category_slug no es None, significa que estamos filtrando por categoria
        categories = get_object_or_404(Category, slug=category_slug) # Obtenemos la categoria por el slug get_object_or_404 recibe el modelo y el slug, si no existe, devuelve un error 404
        products = Product.objects.filter(category=categories, is_available=True).order_by('id') # Filtramos los productos por la categoria y que esten disponibles
        paginator = Paginator(products, 5) #Usamos paginator que recibe la lista de productos y en que divicion seran
        page = request.GET.get('page') # obtenemos el numero de pagina desde la url
        paged_products = paginator.get_page(page) # Devuelve los productos de esa pagina
        product_count = products.count() # Contamos los productos filtrados
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') # Si no estamos filtrando por categoria, obtenemos todos los productos que esten disponibles
        paginator = Paginator(products, 5) #Usamos paginator que recibe la lista de productos y en que divicion seran
        page = request.GET.get('page') # obtenemos el numero de pagina desde la url
        paged_products = paginator.get_page(page) # Devuelve los productos de esa pagina
        product_count = products.count() # Contamos todos los productos disponibles

    context = { # Creamos el contexto que pasaremos a la plantilla
        'products': paged_products, # Lista de productos disponibles
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context) # Renderizamos la plantilla store.html con el contexto creado y request para la solicitud actual


def product_detail(request, category_slug, product_slug): # Vista para mostrar los detalles de un producto
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) # Obtenemos el producto y con __ podemos acceder a las propiedades de su llave foranea asi obtenemos el slug de la categoria
        in_cart= CartItem.objects.filter(cart__cart_id= _cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    
    return render(request, 'store/product_detail.html', context) # Renderizamos la plantilla product_detail.html 

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter( Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)