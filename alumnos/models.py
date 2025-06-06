from django.db import models

# Create your models here.

class ConfiguracionRanking(models.Model):
    titulo_ranking = models.CharField(max_length=200, default="Ranking de Alumnos",
                                      help_text="Título principal que se mostrará en la página del ranking.")

    class Meta:
        verbose_name = "Configuración del Ranking"
        verbose_name_plural = "Configuración del Ranking"

    def __str__(self):
        return "Configuración General del Ranking"

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionRanking.objects.exists():
            raise ValueError("Solo puede existir una instancia de ConfiguracionRanking.")
        super().save(*args, **kwargs)


# class Alumno(models.Model):
#     nombre = models.CharField(max_length=100)
#     puntos_totales = models.IntegerField(default=0)
#     activo = models.BooleanField(default=True)

#     def __str__(self):
#         return self.nombre
    
#     class Meta:
#     # Esto asegura que los alumnos activos siempre aparezcan primero por puntos
#     # y luego por nombre si los puntos son iguales
#         ordering = ['-puntos_totales', 'nombre']

# class Punto(models.Model):
#     alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='puntos_individuales')
#     cantidad = models.IntegerField()
#     fecha_registro = models.DateTimeField(auto_now_add=True)
#     motivo = models.CharField(max_length=200, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         #Actualizar los puntos totales del alumno cada vez que se agrega un punto
#         self.alumno.puntos_totales = self.alumno.puntos_individuales.aggregate(models.Sum('cantidad'))['cantidad__sum'] or 0
#         self.alumno.save()

#     def __str__(self):
#         return f"{self.cantidad} puntos para {self.alumno.nombre}"