from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm): # Creamos un formulario para el registro de usuarios usaando forms.ModelForm que hereda de forms.Form y permite crear formularios basados en modelos de Django.
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingresa tu contraseña',
        'class': 'form-control'
        })) # Campo de contraseña con widget de entrada de contraseña (creamos otro widget)
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirma tu contraseña',
        'class': 'form-control'
    })) # Campo de contraseña de confirmación con widget de entrada de contraseña
    class Meta: # Metadatos del formulario
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        
    def __init__(self, *args, **kwargs): # Creamos el constructor del formulario self para personalizar el formulario, *args y **kwargs para aceptar argumentos adicionales y kwargs para recibir diccionarios de configuración
        super(RegistrationForm, self).__init__(*args, **kwargs) # Llamamos al constructor de la clase padre
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingresa tu nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingresa tu apellido'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingresa tu numero de telefono'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingresa tu correo electronico'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        # Aqui el self hace referencia a la instancia del formulario 
        
    def clean(self): # self es la instancia del formulario(hace referencia a todo el formulario)
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )

