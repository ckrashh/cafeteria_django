from django import forms
from .models import Resena, Cafe, Barista
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

class CafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['nombre', 'origen', 'descripcion','precio', 'nivel_tostado', 'perfil_sabor', 'imagen']  # Ajusta los campos
        labels = {
            'nombre': 'Nombre',
            'origen': 'Origen',
            'descripcion': 'Descripcion',
            'precio': 'Precio',
            'nivel_tostado': 'Nivel Tostado',
            'perfil_sabor': 'Perfil Sabor',
            'imagen': 'Imagen',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
            'perfil_sabor': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nivel_tostado': forms.TextInput(attrs={'class': 'form-control'}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BaristaForm(forms.ModelForm):
    class Meta:
        model = Barista
        fields = ['nombre', 'biografia', 'foto']
        labels = {
            'nombre': 'Nombre',
            'biografia': 'Biografia',
            'foto': 'Foto',
        }
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }