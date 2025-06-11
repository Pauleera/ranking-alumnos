from django import forms
from .models import Partida


class CreatePartidaForm(forms.ModelForm):
    admin_password = forms = forms.CharField(
        max_length=8,
        label= "Contraseña de administrador",
        widget=forms.PasswordInput(attrs={'placeholder':'contraseña para administrar'}),
        required = True
    )
    class Meta:
        model = Partida
        fields = ['nombre']
        labels = {
            'nombre_partida': 'Nombre de la Partida',
        }
        widgets = {
            'nombre_partida': forms.TextInput(attrs={'placeholder': 'Ej: Clase 5A - Matemáticas'})
        }

class AdminLoginForm(forms.Form):
    admin_password = forms.CharField(
        max_length=8,
        label="Contraseña de Administrador",
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce la contraseña'}),
        required=True
    )


# class AlumnoForm(forms.ModelForm):
#     class Meta:
#         model = Alumno
#         fields = ['nombre']

# class PuntoForm(forms.ModelForm):
#     class Meta:
#         model = Punto
#         fields = ['cantidad', 'motivo']
#         widgets = {
#             'cantidad': forms.NumberInput(attrs={'placeholder': 'Puntos', 'min': 1, 'style': 'width: 80px;'}),
#             'motivo': forms.TextInput(attrs={'placeholder': 'Motivo (opcional)', 'style': 'width: 150px;'}),
#         }