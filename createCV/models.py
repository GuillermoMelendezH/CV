from django.db import models

class Perfil(models.Model):
    imagen = models.ImageField(upload_to="perfiles/", blank=True, null=True)
    nombre = models.CharField(max_length=200)
    ine = models.CharField(max_length=20)
    correo = models.EmailField()
    contacto = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(Perfil, related_name="experiencias", on_delete=models.CASCADE)
    empresa = models.CharField(max_length=200)
    puesto = models.CharField(max_length=100) # <- Añade esta línea
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.empresa} ({self.fecha_ingreso} - {self.fecha_salida})"


class Educacion(models.Model):
    perfil = models.ForeignKey(Perfil, related_name="educacion", on_delete=models.CASCADE)
    institucion = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo}"
