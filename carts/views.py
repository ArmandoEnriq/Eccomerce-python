from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Cart, CartItem
from store.models import Product
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
    # Lógica para agregar el producto al carrito
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Verificamos si existe un carrito con ese id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))# Sino existe lo creamos
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) # obtenemos el producto y el codigo del cart
        cart_item.quantity +=1 # En su campo cantidad lo aumentamos
        cart_item.save() # y guardamos
    except CartItem.DoesNotExist: #Sino existe 
        cart_item= CartItem.objects.create( product=product, quantity=1,cart=cart,) # Creamos el objeto cartitem
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id): # Funcion reducir del carrito
    cart= Cart.objects.get(cart_id=_cart_id(request)) #Obtenemos el id
    product = get_object_or_404(Product, id=product_id) #Buscamos si el producto existe
    cart_item= CartItem.objects.get(product=product, cart=cart) #Obtenemos el cart item
    if cart_item.quantity>1: # Si en su campo quantity es mayor a 1 
        cart_item.quantity -= 1 # Entonces reducimos 1
        cart_item.save() # GUardamos
    else:
        cart_item.delete() #Si es menor borramos
    return redirect('cart')


def remove_cart_item(request, product_id): # Funcion eliminar de CartItem
    cart = Cart.objects.get(cart_id=_cart_id(request)) #Obtenemos el id del carrito 
    product = get_object_or_404(Product,id=product_id) # Obtenemos el producto si existe
    cart_item = CartItem.objects.get(product=product, cart=cart) #Obtenemos el cartitem
    cart_item.delete() # Borramos el item 
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    """
    Vista para mostrar el carrito de compras.
    Aquí se pueden agregar productos, eliminar productos, etc.
    """
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