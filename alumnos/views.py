from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import ConfiguracionRanking


def alumno_ranking_view(request):
    titulo_ranking = "Ranking de Alumnos" # Valor por defecto si no usas ConfiguracionRanking
    try:
        config = ConfiguracionRanking.objects.get()
        titulo_ranking = config.titulo_ranking
    except ConfiguracionRanking.DoesNotExist:
        pass # Si no existe, usamos el valor por defecto

    return render(request, 'alumnos/alumno_ranking.html', {'titulo_ranking': titulo_ranking})

# # Esta vista manejará la adición de puntos desde el formulario incrustado
# def add_points_inline(request):
#     if request.method == 'POST':
#         form = PuntoForm(request.POST)
#         if form.is_valid():
#             alumno_id = request.POST.get('alumno_id') # Obtenemos el ID del alumno del campo oculto
#             alumno = get_object_or_404(Alumno, pk=alumno_id, activo=True)
#             punto = form.save(commit=False)
#             punto.alumno = alumno
#             punto.save()
#             return redirect('alumno_ranking') # Redirige de nuevo al ranking
#     # Si no es POST o el formulario no es válido, se debería mostrar un error o redirigir
#     # Para este caso simple, siempre redirigiremos al ranking si algo va mal o no es POST
#     return redirect('alumno_ranking')

# # Mantendremos AlumnoCreateView por si quieres una página dedicada para crear alumnos
# class AlumnoCreateView(CreateView):
#     model = Alumno
#     form_class = AlumnoForm
#     template_name = 'alumnos/alumno_form.html'
#     success_url = reverse_lazy('alumno_ranking')

# # Nueva vista para "eliminar" un alumno (borrado suave)
# def alumno_eliminar(request, pk):
#     alumno = get_object_or_404(Alumno, pk=pk)
#     if request.method == 'POST':
#         alumno.activo = False # Marca el alumno como inactivo
#         alumno.save()
#         # Opcional: Si quieres recalcular los puntos de todos los alumnos
#         # para asegurarte de que el ranking se actualice correctamente si hay dependencias complejas.
#         # Aunque con el cambio de `queryset` en AlumnoRankingView, debería ser suficiente.
#         return redirect('alumno_ranking')
#     # Para un simple GET a la página de eliminación, puedes mostrar una confirmación
#     return render(request, 'alumnos/alumno_confirm_delete.html', {'alumno': alumno})
