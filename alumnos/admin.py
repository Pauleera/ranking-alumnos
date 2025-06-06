from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ConfiguracionRanking


@admin.register(ConfiguracionRanking)
class ConfiguracionRankingAdmin(admin.ModelAdmin):
    list_display = ('titulo_ranking',)
    def has_add_permission(self, request): return not ConfiguracionRanking.objects.exists()
    def has_delete_permission(self, request, obj=None): return False

# @admin.register(Alumno)
# class AlumnoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'puntos_totales')
#     search_fields = ('nombre',)

# @admin.register(Punto)
# class PuntoAdmin(admin.ModelAdmin):
#     list_display = ('alumno', 'cantidad', 'fecha_registro', 'motivo')
#     list_filter = ('fecha_registro', 'alumno')
#     search_fields = ('alumno__nombre', 'motivo')