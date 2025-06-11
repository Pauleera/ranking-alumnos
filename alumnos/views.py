from django.shortcuts import render, redirect, get_object_or_404
# from .models import ConfiguracionRanking
from django.urls import reverse
from .models import Partida, Alumno
from django import forms 
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F # Operaciones atómicas


class CreatePartidaForm(forms.Form):
    nombre_partida = forms.CharField(
        max_length=200,
        label='Nombre de la Partida',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Programación Competitiva - UdeC'})
    )
    admin_password = forms = forms.CharField(
        max_length=4,
        label= "Contraseña de administrador",
        widget=forms.PasswordInput(attrs={'placeholder':'contraseña para administrar'})
    )

class AdminLoginForm(forms.Form):
    admin_password = forms.CharField(
        max_length=100,
        label="Contraseña de Administrador",
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce la contraseña'})
    )



def home_view(request):
    return render(request, 'alumnos/home.html')

def create_partida_view(request):
    
    if request.method == 'POST':
        form = CreatePartidaForm(request.POST)
        if form.is_valid():
            partida = form.save(commit=False) #Obtener partida, sin guardarla


            while True:
                new_short_code = get_random_string(length=4).upper()
                if not Partida.objects.filter(short_code = new_short_code).exists():
                    partida.short_code = new_short_code
                    break

            nombre = form.cleaned_data['nombre_partida']
            raw_password = form.cleaned_data['admin_password']
            if raw_password:
                partida.set_admin_password(raw_password)


            partida.save()

            request.session[f'admin_logged_in_{partida.id}'] = True

            return redirect(reverse('alumnos:admin_dashboard', args=[partida.id]))
    else:
        form = CreatePartidaForm()
    return render(request, 'alumnos/create_partida.html', {'form': form})


def leaderboard_view(request, short_code):
    partida = get_object_or_404(Partida, short_code=short_code)
    alumnos = partida.alumnos.all()
    return render(request, 'alumnos/leaderboard.html',{
        'partida': partida,
        'partida_id': str(partida.id),
        'short_code': short_code,
    })

def admin_login_view(request, short_code):
    partida = get_object_or_404(Partida, short_code=short_code)
    error_message = None

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data['admin_password']
            if partida.check_admin_password(raw_password):
                request.session[f'admin_logged_in_{partida.id}'] = True
                return redirect(reverse('alumnos:admin_dashboard', args=[partida.id]))
            else:
                error_message = "Contraseña incorrecta."
    else:
        form = AdminLoginForm()
    return render(request, 'alumnos/admin_login.html', {
        'form': form,
        'partida': partida,
        'short_code': short_code, 
        'error_message': error_message
    })


def admin_dashboard_view(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if not request.session.get(f'admin_logged_in_{partida.id}'):
        return redirect(reverse('alumnos:admin_login', args=[partida.short_code]))
    
    return render(request, 'alumnos/admin_dashboard.html',{
        'partida': partida,
        'partida_id': str(partida.id),
        'short_code': partida.short_code
    })


@csrf_exempt
def add_alumno_api(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    # Verifica la autenticación del administrador para esta partida
    if not request.session.get(f'admin_logged_in_{partida_id}'):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre_alumno = data.get('nombre_alumno')
            if not nombre_alumno:
                return JsonResponse({'success': False, 'error': 'Nombre de alumno es requerido'}, status=400)

            # Crea el alumno y lo asocia a la partida
            alumno, created = Alumno.objects.get_or_create(partida=partida, nombre=nombre_alumno, defaults={'puntos': 0})

            if not created:
                return JsonResponse({'success': False, 'error': 'Ya existe un alumno con ese nombre en esta partida.'}, status=409)

            return JsonResponse({
                'success': True,
                'alumno': {
                    'id': alumno.id,
                    'nombre': alumno.nombre,
                    'puntos': alumno.puntos
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@csrf_exempt
def update_points_api(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if not request.session.get(f'admin_logged_in_{partida_id}'):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alumno_id = data.get('alumno_id')
            points_change = int(data.get('points_change', 0))

            if not alumno_id:
                return JsonResponse({'success': False, 'error': 'ID de alumno es requerido'}, status=400)

            # Usar F() para asegurar operaciones atómicas
            alumno = get_object_or_404(Alumno, id=alumno_id, partida=partida)
            alumno.puntos = F('puntos') + points_change
            alumno.save()
            alumno.refresh_from_db() # Recargar el objeto para obtener el nuevo valor de puntos

            return JsonResponse({
                'success': True,
                'alumno': {
                    'id': alumno.id,
                    'nombre': alumno.nombre,
                    'puntos': alumno.puntos
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'points_change debe ser un número entero'}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@csrf_exempt
def partida_data_api(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    # Obtener alumnos ordenados por puntos
    alumnos_data = list(Alumno.objects.filter(partida=partida).order_by('-puntos', 'nombre').values('id', 'nombre', 'puntos'))

    # Calcular tiempo restante del temporizador
    remaining_time = 0
    if partida.timer_is_running and partida.timer_start_time:
        from django.utils import timezone
        elapsed_time = (timezone.now() - partida.timer_start_time).total_seconds()
        remaining_time = max(0, partida.timer_duration_seconds - int(elapsed_time))
    elif not partida.timer_is_running:
        remaining_time = partida.timer_paused_at_seconds

    return JsonResponse({
        'success': True,
        'partida': {
            'id': str(partida.id),
            'nombre': partida.nombre,
            'timer_duration_seconds': partida.timer_duration_seconds,
            'timer_start_time': partida.timer_start_time.isoformat() if partida.timer_start_time else None,
            'timer_paused_at_seconds': partida.timer_paused_at_seconds,
            'timer_is_running': partida.timer_is_running,
            'remaining_time_seconds': remaining_time
        },
        'alumnos': alumnos_data
    })


@csrf_exempt
def timer_action_api(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if not request.session.get(f'admin_logged_in_{partida_id}'):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action') # 'start', 'pause', 'reset', 'set_duration'
            from django.utils import timezone

            if action == 'set_duration':
                duration = int(data.get('duration', 0))
                if duration < 0:
                    return JsonResponse({'success': False, 'error': 'La duración no puede ser negativa.'}, status=400)
                partida.timer_duration_seconds = duration
                if not partida.timer_is_running: # Si no está corriendo, también actualiza los segundos pausados
                    partida.timer_paused_at_seconds = duration
                partida.save()
            elif action == 'start':
                if not partida.timer_is_running:
                    # Calcular el nuevo start_time para que el timer continúe desde donde se pausó
                    partida.timer_start_time = timezone.now() - timezone.timedelta(seconds=partida.timer_duration_seconds - partida.timer_paused_at_seconds)
                    partida.timer_is_running = True
                    partida.save()
            elif action == 'pause':
                if partida.timer_is_running:
                    elapsed = (timezone.now() - partida.timer_start_time).total_seconds()
                    partida.timer_paused_at_seconds = max(0, partida.timer_duration_seconds - int(elapsed))
                    partida.timer_is_running = False
                    partida.save()
            elif action == 'reset':
                partida.timer_is_running = False
                partida.timer_start_time = None
                partida.timer_paused_at_seconds = partida.timer_duration_seconds # Resetea al total
                partida.save()
            else:
                return JsonResponse({'success': False, 'error': 'Acción de temporizador no válida'}, status=400)

            # Devolver el estado actualizado de la partida (incluyendo el temporizador)
            return JsonResponse({
                'success': True,
                'partida': {
                    'id': str(partida.id),
                    'nombre': partida.nombre,
                    'timer_duration_seconds': partida.timer_duration_seconds,
                    'timer_start_time': partida.timer_start_time.isoformat() if partida.timer_start_time else None,
                    'timer_paused_at_seconds': partida.timer_paused_at_seconds,
                    'timer_is_running': partida.timer_is_running,
                    'remaining_time_seconds': partida.timer_paused_at_seconds if not partida.timer_is_running else max(0, partida.timer_duration_seconds - int((timezone.now() - partida.timer_start_time).total_seconds()))
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Duración debe ser un número entero válido'}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)




# def alumno_ranking_view(request):
#     titulo_ranking = "Ranking de Alumnos" # Valor por defecto si no usas ConfiguracionRanking
#     try:
#         config = ConfiguracionRanking.objects.get()
#         titulo_ranking = config.titulo_ranking
#     except ConfiguracionRanking.DoesNotExist:
#         pass # Si no existe, usamos el valor por defecto

#     return render(request, 'alumnos/alumno_ranking.html', {'titulo_ranking': titulo_ranking})

