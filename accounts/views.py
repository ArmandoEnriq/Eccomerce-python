# Contiene la lógica para:
# Registro de usuarios (signup).
# Inicio de sesión (login).
# Cierre de sesión (logout).
# Edición de perfil (profile_update).

from django.shortcuts import render, redirect # Importamos las funciones render(para renderizar templates) y redirect(para redirigir a otras vistas)
from .forms import RegistrationForm # Importamos el formulario RegistrationForm
from .models import Account # Importamos el modelo Account
from django.contrib import messages, auth # Importamos el modulo messages(para mostrar mensajes) y auth(para autenticar usuarios)
from django.contrib.auth.decorators import login_required # Importamos el decorador login_required (para verificar si el usuario esta autenticado)
from django.contrib.sites.shortcuts import get_current_site # Importamos el modulo get_current_site (para obtener la url de la pagina actual)
from django.template.loader import render_to_string # Importamos el modulo render_to_string (para renderizar templates)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # Importamos las funciones urlsafe_base64_encode y urlsafe_base64_decode (para codificar y decodificar el id del usuario)
from django.utils.encoding import force_bytes # Importamos la funcion force_bytes (para codificar el id del usuario)
from django.contrib.auth.tokens import default_token_generator # Importamos el modulo default_token_generator (para generar el token de activacion)
from django.core.mail import EmailMessage # Importamos el modulo EmailMessage (para enviar emails)
from django.urls import reverse

# Create your views here.

def register(request):
    
    form = RegistrationForm()
    if request.method == 'POST': # Si el metodo es post
        form = RegistrationForm(request.POST) # Creamos el formulario con los datos del post
        if form.is_valid(): # Si el formulario es valido
            first_name = form.cleaned_data['first_name'] #cleaned_data es un diccionario con los datos limpios ejemplo first_name = 'jose' cleaned_data = {'first_name': 'jose'}
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0] # Se obtiene el nombre de usuario a partir del correo electronico ejemplo jose@jose.com username = 'jose'
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password) # Creamos el usuario
            user.phone_number = phone_number # Establecemos el numero de telefono
            user.save() # Guardamos el usuario
            # Creamos la referencia de activacion del correo electronico
            current_site= get_current_site(request) # Obtenemos el sitio actual(la url de la pagina)
            mail_subject = 'Por favor activa tu cuenta' # Asunto del correo
            body = render_to_string('accounts/account_verification_email.html', { #Creamos el cuerpo del correo definido en el archivo account_verification_email.html
                'user': user, # Enviamos el usuario
                'domain': current_site, # Enviamos el sitio actual la url de la pagina
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # Enviamos el id del usuario usando la urlsafe_base64_encode para codificar el id
                'token': default_token_generator.make_token(user), # Enviamos el token usando el default_token_generator para generar el token usando el id del usuario
            })
            to_email = email #almacena el correo electronico del usuario
            send_email = EmailMessage(mail_subject, body, to=[to_email]) # Creamos el objeto que envia el correo usando el asunto, el cuerpo y el destinatario
            send_email.send() # Enviamos el correo
            
            
            
            messages.success(request, 'Cuenta creada exitosamente')
            form = RegistrationForm() # Limpiamos el formulario
            return redirect(reverse('login') + '?command=verification&email=' + email)
 # Redirigimos a la vista login con el email del usuario para que envie el correo
    
    context = {
        'form': form
        }
    return render(request, 'accounts/register.html', context)

def login(request):  # Creamos la vista login
    
    if request.method=='POST': # Si el metodo es post
        email = request.POST['email'] # Obtenemos el email del formulario
        password = request.POST['password'] # Obtenemos la password del formulario
        
        user = auth.authenticate(email=email, password=password) # usamos la funcion auth.authenticate para autenticar el usuario
        
        if user is not None:
            auth.login(request, user) # usamos la funcion auth.login para iniciar sesion la cual recibe el request y el usuario
            messages.success(request, 'Has iniciado sesion correctamente')
            return redirect('dashboard')
        else:
            messages.error(request, 'Las credenciales no son correctas')
            return redirect('login')
    
    
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    
    auth.logout(request)
    messages.success(request, 'Has cerrado sesion')
    return redirect('login')


def activate(request, uidb64, token): # Creamos la vista para activar la cuenta
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # Decodificamos el id del usuario usando la urlsafe_base64_decode
        user = Account._default_manager.get(pk=uid) # Obtenemos el usuario usando el id decodificado
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist): # Si el id del usuario no es valido
        user = None
    if user is not None and default_token_generator.check_token(user, token): # Si el id del usuario es valido y el token es valido
        user.is_active = True # Establecemos el campo is_active a True para indicar que el usuario esta activo
        user.save() # Guardamos el usuario
        messages.success(request, 'Cuenta activada correctamente')
        return redirect('login')
    else:
        messages.error(request, 'El link de activacion es invalido')
        return redirect('register')
    
    
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request): # Creamos la vista forgotPassword
    if request.method=='POST': # Si el metodo es post
        email = request.POST['email'] # Obtenemos el email del formulario
        if Account.objects.filter(email=email).exists(): # Si el email existe
            user = Account.objects.get(email__exact=email) # Obtenemos el usuario usando el email__exact (el doble guion es un operador de busqueda) para buscar el email exacto
            current_site = get_current_site(request) # Obtenemos el sitio actual
            mail_subject = 'Reseteat Password' # Asunto del correo
            body =render_to_string('accounts/reset_password_email.html',{ # Creamos el cuerpo del correo definido en el archivo reset_password_email.html
                'user': user, # Enviamos el usuario
                'domain': current_site, # Enviamos el sitio actual (la url de la pagina)
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # Enviamos el id del usuario usando la urlsafe_base64_encode para codificar el id
                'token': default_token_generator.make_token(user), # Enviamos el token usando el default_token_generator para generar el token usando el id del usuario
            })
            to_email = email #almacena el correo electronico del usuario
            send_email= EmailMessage(mail_subject,body, to=[to_email]) # Creamos el correo usando el asunto, el cuerpo y el destinatario
            send_email.send() # Enviamos el correo
            
            messages.success(request, 'Un email fue enviado para confirmar su correo')
            return redirect('login')
        else:
            messages.error(request,'La cuenta esta en verificacion sino le llega nada no existe ')
            return redirect('forgotPassword')
    
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token): # Creamos la vista resetpassword_validate (para validar el token)
        try: 
            uid= urlsafe_base64_decode(uidb64).decode() # Decodificamos el id del usuario
            user = Account._default_manager.get(pk=uid) # Obtenemos el usuario usando el manager por defecto y la llave primaria que es el id
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist): # Si el id del usuario no es valido
            user = None 

        if user is not None and default_token_generator.check_token(user,token): # Si el id del usuario es valido y el token es valido
            request.session['uid']= uid # Guardamos el id del usuario en la sesion
            messages.success(request, 'Porfavor resetea tu Contraseña') 
            return redirect ('resetPassword')
        else:
            messages.error(request, 'El link ha expirado')
            return redirect('login')
    
def resetPassword(request): # Creamos la vista resetPassword (para resetear la contraseña)
    if request.method == 'POST': # Si el metodo es post
        password = request.POST['password'] # Obtenemos la password del formulario
        confirm_password = request.POST['confirm_password'] # Obtenemos la confirmacion de la password
        
        if password == confirm_password: # Si la password y la confirmacion de la password son iguales
            uid = request.session.get('uid') # Obtenemos el id del usuario
            user = Account.objects.get(pk=uid) # Obtenemos el usuario
            user.set_password(password) # Usamos la funcion set_password para cambiar la contraseña
            user.save()
            messages.success(request, 'La contraseña se ha cambiado correctamente')
            return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')