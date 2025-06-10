from django.contrib import admin

# Register your models here.
from .models import Partida, Alumno
from django.contrib.auth.hashers import make_password
from django import forms


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id', 'created_at', 'updated_at', 'timer_is_running')
    search_fields = ('nombre', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at', 'admin_password_hash') # ID no editable, hash no directo

    # Añadir un campo temporal para la contraseña en el formulario del admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None: # Solo al crear una nueva partida
            form.base_fields['raw_admin_password'] = forms.CharField(label="Contraseña de Administrador (nueva)", widget=forms.PasswordInput, required=True)
        return form

    # Sobreescribir save_model para hashear la contraseña
    def save_model(self, request, obj, form, change):
        if 'raw_admin_password' in form.cleaned_data and form.cleaned_data['raw_admin_password']:
            obj.set_admin_password(form.cleaned_data['raw_admin_password'])
        super().save_model(request, obj, form, change)

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos', 'partida', 'created_at')
    list_filter = ('partida',) # Permite filtrar alumnos por partida
    search_fields = ('nombre',)
    raw_id_fields = ('partida',) # Para facilitar la selección de la partida en el admin
    readonly_fields = ('created_at', 'updated_at')


# @admin.register(ConfiguracionRanking)
# class ConfiguracionRankingAdmin(admin.ModelAdmin):
#     list_display = ('titulo_ranking',)
#     def has_add_permission(self, request): return not ConfiguracionRanking.objects.exists()
#     def has_delete_permission(self, request, obj=None): return False
