from django.urls import path
from .views import alumno_ranking_view

urlpatterns = [
    path('', alumno_ranking_view, name='alumno_ranking'),
    # path('nuevo/', AlumnoCreateView.as_view(), name='alumno_nuevo'),
    # path('sumar-puntos-inline/', add_points_inline, name='sumar_puntos_inline'),
    # path('<int:pk>/eliminar/', alumno_eliminar, name='alumno_eliminar'),
]