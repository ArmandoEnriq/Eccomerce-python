# Configuración del panel de administración
from django.contrib import admin
from .models import Account  # Importamos el modelo Account
from django.contrib.auth.admin import UserAdmin 


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active') # Definimos los campos que se mostrarán en la lista de usuarios
    list_display_links = ('email', 'first_name', 'last_name') # Definimos los campos que serán enlaces a la página de edición del usuario
    readonly_fields = ('date_joined', 'last_login') # Definimos los campos que serán de solo lectura
    ordering = ('-date_joined',) # Definimos el orden en que se mostrarán los usuarios
    
    filter_horizontal = ()  # Campos que no se mostrarán en la lista de usuarios
    list_filter = ()  # Campos que se mostrarán como filtros en la lista de usuarios
    fieldsets = ()  # Campos que se mostrarán en la página de edición del usuario

# Register your models here.
admin.site.register(Account, AccountAdmin) # Registramos el modelo Account en el panel de administración de Django
 