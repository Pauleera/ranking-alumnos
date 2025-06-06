from django import forms

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