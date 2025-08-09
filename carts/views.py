from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request): # Creamos una funcion que crea una sesion unica pero si ya se habia creado la retorna
    """
    Función para obtener el ID del carrito de la sesión.
    Si no existe, se crea uno nuevo.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 

def add_cart(request, product_id):
    """
    Vista para agregar un producto al carrito.
    Aquí se puede implementar la lógica para añadir productos al carrito.
    """
    product = Product.objects.get(id=product_id)  # Obtiene el producto por su ID
    
    product_variation = [] # Creamos una lista para las variaciones
    if request.method == 'POST': # Si el metodo es post
        for item in request.POST:# Recorremos las variaciones
            key = item # Obtenemos la key
            value = request.POST[key] # Obtenemos el value
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value) # Obtenemos las variaciones donde el producto sea igual al producto, variation_category sea igual a key sin importar mayusculas y variation_value sea igual a value sin importar mayusculas
                product_variation.append(variation) # Agregamos la variacion
            except: 
                pass # Sino pasa nada
    
    
    # Lógica para agregar el producto al carrito
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Verificamos si existe un carrito con ese id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))# Sino existe lo creamos
    cart.save() 
    
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists() # Verificamos si el producto ya existe en el carrito
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart) # obtenemos el producto y el codigo del cart
        
        ex_var_list = [] # Creamos una lista para las variaciones
        id = [] # Creamos una lista para los id
        for item in cart_item: # Para cada item
            existing_variations = item.variations.all() # Obtenemos las variaciones
            ex_var_list.append(list(existing_variations)) # Agregamos las variaciones a la lista
            id.append(item.id) # Agregamos el id de cada item (cartitem) a la lista
        if product_variation in ex_var_list: # Si la variacion que llego por post esta en la lista de variaciones del producto en cartitem
            index = ex_var_list.index(product_variation) # Obtenemos el index de la variacion
            item_id = id[index] # Obtenemos el id del item
            item = CartItem.objects.get(product=product, id=item_id) # Obtenemos el cart item
            item.quantity += 1 # Sumamos 1
            item.save() # Guardamos
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation)>0: # Si la longitud de las variaciones que llego por post es mayor a 0 (si tiene variaciones talla y color)
                cart_item.variations.clear() # Limpiamos solo por si acaso pero al ser nuevo es redundante
                item.variations.add(*product_variation) # con * le decimos que agregue todo desempaqueta el objeto var1, var2] a var1, var2)
            item.save()
        
    else:
        cart_item= CartItem.objects.create( product=product, quantity=1,cart=cart,) # Creamos el objeto cartitem
        if len(product_variation)>0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id): # Funcion reducir del carrito
    cart= Cart.objects.get(cart_id=_cart_id(request)) #Obtenemos el id
    product = get_object_or_404(Product, id=product_id) #Buscamos si el producto existe
    try:
        cart_item= CartItem.objects.get(product=product, cart=cart, id=cart_item_id) #Obtenemos el cart item
        if cart_item.quantity>1: # Si en su campo quantity es mayor a 1 
            cart_item.quantity -= 1 # Entonces reducimos 1
            cart_item.save() # GUardamos
        else:
            cart_item.delete() #Si es menor borramos
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id): # Funcion eliminar de CartItem
    cart = Cart.objects.get(cart_id=_cart_id(request)) #Obtenemos el id del carrito 
    product = get_object_or_404(Product,id=product_id) # Obtenemos el producto si existe
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) #Obtenemos el cartitem
    cart_item.delete() # Borramos el item 
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    """
    Vista para mostrar el carrito de compras.
    Aquí se pueden agregar productos, eliminar productos, etc.
    """
    tax = 0 # Creamos una variable para el iva
    grand_total = 0 # Creamos una variable para el total
    try:
        cart= Cart.objects.get(cart_id=_cart_id(request))  # Obtenemos el id del carrito
        cart_items= CartItem.objects.filter(cart=cart, is_active=True) # Obtenemos los productos del cartItem donde tengan el mismo id del carrito
        for cart_item in cart_items: #para cada producto
            total += (cart_item.product.price * cart_item.quantity) # multuplicaremos su cantidad por su precio
            quantity += cart_item.quantity #Sumaremos los items
        tax = total * Decimal('0.16') # Sacaremos el % de iva
        grand_total = total * Decimal('1.16') # sumaremos el total por el iva
    except ObjectDoesNotExist: # Sino existe 
        pass # Pasaremos 
    
    context = { # Pasaremos el contexto de la variables
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'store/cart.html', context)