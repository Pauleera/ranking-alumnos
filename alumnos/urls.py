from django.urls import path
from . import views
#from .views import alumno_ranking_view

app_name = 'alumnos'

urlpatterns = [
    #Pagina inicio crear o unirse
    path('' , views.home_view, name='home'),

    path('partida/crear/', views.create_partida_view, name = 'create_partida'),

    path('partida/codigo/<str:short_code>/', views.leaderboard_view, name = 'leaderboard'),
    path('partida/codigo/<str:short_code>/admin/', views.admin_login_view, name='admin_login'),
    path('partida/<uuid:partida_id>/admin/dashboard/' , views.admin_dashboard_view, name = 'admin_dashboard'),

    #ENDPOINT API
    path('api/partida/<uuid:partida_id>/add_alumno/', views.add_alumno_api, name='api_add_alumno'),
    path('api/partida/<uuid:partida_id>/update_points/', views.update_points_api, name='api_update_points'),
    path('api/partida/<uuid:partida_id>/data/', views.partida_data_api, name='api_partida_data'),
    path('api/partida/<uuid:partida_id>/timer_action/', views.timer_action_api, name='api_timer_action'),
    

]