from django.db import models
import uuid 
from django.contrib.auth.hashers import make_password, check_password
import random
import string

# Create your models here.

class Partida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID único para compartir la partida" )
    nombre = models.CharField(max_length=200 , help_text="Nombre de la partida (ej. 'Competencia de Programación').")
    admin_password_hash = models.CharField(max_length=128, help_text="contraseña para administrar la partida")
    short_code = models.CharField(max_length=8, unique=True, blank=True, null=True)

    #Temporizador
    timer_duration_seconds = models.IntegerField(default= 0 , help_text= "Duración total del temporizador en segundos. (0=sin temporizador)")
    timer_start_time = models.DateTimeField(null = True, blank=True, help_text="Momento en que el temporizador fue iniciado por última vez")
    timer_paused_at_seconds = models.IntegerField(default = 0 , help_text="Segundos restantes cuando el temporizador fue pausado")
    timer_is_running = models.BooleanField(default = False, help_text="Indica si el temporizador está actualmente en ejecución")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name = "Partida de Ranking"
        verbose_name_plural = "Partidas de Ranking"
        ordering = ['-created_at']

    def set_admin_password(self, raw_password ):
        self.admin_password_hash = make_password(raw_password)
    
    def check_admin_password(self, raw_password):
        return check_password(raw_password, self.admin_password_hash)
    
    def generate_unique_short_code(self, length=4): # Puedes ajustar la longitud aquí
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choice(characters) for i in range(length))
            if not Partida.objects.filter(short_code=code).exists():
                return code
    
    def save(self, *args, **kwargs):
        if not self.short_code: # Genera el código solo si no existe
            self.short_code = self.generate_unique_short_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    


class Alumno(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='alumnos', help_text = 'Partida a la que pertenece este alumno.')
    nombre = models.CharField(max_length=100)
    puntos = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        unique_together = ('partida', 'nombre')
        ordering = ['-puntos', 'nombre']


    def __str__(self):
        return f"{self.nombre} ({self.puntos} puntos) - Partida: {self.partida.nombre}  "
 





# class ConfiguracionRanking(models.Model):
#     titulo_ranking = models.CharField(max_length=200, default="Ranking de Alumnos",
#                                       help_text="Título principal que se mostrará en la página del ranking.")

#     class Meta:
#         verbose_name = "Configuración del Ranking"
#         verbose_name_plural = "Configuración del Ranking"

#     def __str__(self):
#         return "Configuración General del Ranking"

#     def save(self, *args, **kwargs):
#         if not self.pk and ConfiguracionRanking.objects.exists():
#             raise ValueError("Solo puede existir una instancia de ConfiguracionRanking.")
#         super().save(*args, **kwargs)

