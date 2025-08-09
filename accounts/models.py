# Modelos de la base de datos (usuarios personalizados, perfiles)
# Usuario personalizado (si reemplazas el modelo User por defecto de Django).
# Perfiles de usuario (ej: Profile con campos adicionales como avatar, teléfono, etc.).
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # Importamos las clases necesarias para crear un modelo de usuario personalizado, usamos AbstractBaseUser para crear un modelo de usuario personalizado, PermissionsMixin para agregar permisos al usuario y BaseUserManager para crear un administrador de usuarios personalizado.

# Create your models here.

class MyAccountManager(BaseUserManager): # Creamos la clase MyAccountManager que hereda de BaseUserManager los métodos necesarios para crear un administrador de usuarios personalizado.
    def create_user(self, email, username, first_name, last_name, password=None): # Creamos el método create_user que recibe los parámetros necesarios para crear un usuario.
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        
        user = self.model( # Creamos una instancia del modelo de usuario con los parámetros recibidos.
            email=self.normalize_email(email), # Convertimos a minusculas usando un metodo del manager(self)
            username=username, # Parámetro directo
            first_name=first_name,
            last_name=last_name
        )
         # 3. Manejar la contraseña (fuera de self.model)
        user.set_password(password) # Establecemos la contraseña del usuario, si se proporciona usando un Método del modelo (AbstractBaseUser)
        user.save(using=self._db) # ¡Aquí se validan todos los campos del modelo! y si cumple Guardar en la BD (self._db es la BD configurada en el manager)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, password): # Creamos el método create_superuser que recibe los parámetros necesarios para crear un superusuario.
        user = self.create_user( # Creamos un usuario normal con los parámetros recibidos.
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
    
        user.is_admin = True # Establecemos el campo is_admin a True para indicar que es administrador.
        user.is_staff = True # Establecemos el campo is_staff a True para indicar que es miembro del personal.
        user.is_active = True # Establecemos el campo is_active a True para indicar que el usuario está activo.
        user.is_superadmin = True # Establecemos el campo is_superadmin a True para indicar que es un superadministrador.
        user.save(using=self._db) # Verifica ¡Aquí que se validan todos los campos del modelo! y si cumple Guardamos el superusuario en la base de datos.
        return user


class Account(AbstractBaseUser): # Creamos la clase Account que hereda de AbstractBaseUser (para funcionalidad básica de autenticación) y PermissionsMixin (para permisos).
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    
    #Campos atributos
    date_joined = models.DateTimeField(auto_now_add=True) # Fecha de creación del usuario
    last_login = models.DateTimeField(auto_now=True) # Fecha del último inicio de sesión
    is_admin = models.BooleanField(default=False) # Campo para verificar si el usuario es administrador
    is_staff = models.BooleanField(default=False) # Campo para verificar si el usuario es miembro del personal
    is_active = models.BooleanField(default=False) # Campo para verificar si el usuario está activo
    is_superadmin = models.BooleanField(default=False) # Campo para verificar si el usuario es superadministrador
    
    USERNAME_FIELD = 'email' # Definimos el campo que se usará para iniciar sesión
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] # Campos obligatorios
    
    objects = MyAccountManager() # Asignamos el administrador de usuarios personalizado modificando el comportamiento del modelo primero validara los datos y luego lo creara es como un midleware
    '''Cuando creamos un usuario nuevo seria dentro asi user = Account.objects.create_user(email="a@b.com", username="test", ...) lo que hacemos es remplazar el object por defecto al MyAccountManager que creamos'''
    
    def __str__(self):
        return self.email # Devuelve el email como identificador principal del usuario en el panel de administracion 
    
    def has_perm(self, perm, obj=None): # has_perm Controla permisos a nivel de modelo/acción.
        return self.is_admin # Verifica si el usuario tiene permisos de admin
    
    def has_module_perms(self, add_label):  # Controla acceso a módulos completos en el admin.
        #app_label: Nombre de la aplicación (ej: 'store', 'auth').
        return True # Verifica si el usuario tiene permisos para acceder a una app específica. regresa true puede acceder a todas 