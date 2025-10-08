from django import forms
from .models import Resena
from django.contrib.auth.models import Group
from sesion.models import CustomUser

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['nombre_cliente', 'comentario', 'calificacion']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

class CambiarGrupoForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,  # Permite enviar el formulario sin seleccionar un grupo
        empty_label="Eliminar grupos",  # Opción en blanco
        label="Seleccionar Grupo"
    )

    class Meta:
        model = CustomUser
        fields = []  # No necesitas campos del modelo, solo el grupo

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']  # Campos editables
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }
