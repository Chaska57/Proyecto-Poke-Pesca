from django.db import models
from PIL import Image
from django.contrib.auth.models import User
import os


class Distribution(models.Model):
    description = models.CharField(max_length=500, verbose_name="Descripción de la Distribución")

    class Meta:
        verbose_name = "Distribución"
        verbose_name_plural = "Distribuciones"

    def __str__(self):
        return self.description[:50]

class Diet(models.Model):
    description = models.CharField(max_length=500, verbose_name="Descripción de la Alimentación")

    class Meta:
        verbose_name = "Alimentación"
        verbose_name_plural = "Alimentaciones"

    def __str__(self):
        return self.description[:50]

class Fish(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    scientific_name = models.CharField(max_length=255, verbose_name="Nombre Científico")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    image = models.ImageField(upload_to='fish_images', null=True, blank=True, verbose_name="Imagen del Pez")
    tier = models.CharField(
        max_length=50, 
        choices=[
            ('SS', 'SS'),
            ('S', 'S'),
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            
        ],
        verbose_name="Tiers")
    
    class Meta:
        verbose_name = "Pez"
        verbose_name_plural = "Peces"

    def save(self, *args, **kwargs):
        # Redimensionar la imagen antes de guardarla
        if self.image:
            img = Image.open(self.image)
            
            # Obtener las dimensiones originales de la imagen
            width, height = img.size
            
            # Calcular el alto que corresponde con la proporción 5:4
            new_width = 500
            new_height = int(new_width * 4 / 5)  # Proporción 5:4
            
            # Calcular la parte de la imagen que se va a recortar
            left = 0  # Puedes cambiar esto para mover el recorte horizontalmente
            upper = (height - new_height) // 2  # Centrar el recorte verticalmente
            right = new_width
            lower = upper + new_height
            
            # Realizar el recorte
            img = img.crop((left, upper, right, lower))
            
            # Guardar la imagen recortada
            img.save(self.image.path)
        
        super().save(*args, **kwargs)  # Guardar el modelo

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    photo = models.ImageField(upload_to='user_photos', verbose_name="Foto del Usuario")
    fishes = models.ManyToManyField('Fish', through='UserFish', related_name='users', verbose_name="Peces Capturados")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.photo:
            img = Image.open(self.photo)
            
            # Redimensionar la imagen, asegurándose de que el lado más corto sea de 500px
            img.thumbnail((500, 500))  # Mantener la relación de aspecto y ajustar al tamaño máximo
            
            # Obtener las nuevas dimensiones después de redimensionar
            width, height = img.size
            
            # Calcular el recorte cuadrado de 500x500px centrado
            left = (width - 500) // 2
            upper = (height - 500) // 2
            right = left + 500
            lower = upper + 500

            # Recortar la imagen para mantener el cuadrado centrado
            img = img.crop((left, upper, right, lower))
            
            # Guardar la imagen recortada en la misma ruta
            img.save(self.photo.path)

        super(User, self).save(*args, **kwargs)

class UserFish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, verbose_name="Pez")
    captured = models.BooleanField(default=False, verbose_name="Capturado")
    size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Tamaño (cm)")  # Tamaño en cm
    weight = models.IntegerField(null=True, blank=True, verbose_name="Peso (gramos)")  # Peso en gramos (enteros)
    location = models.CharField(max_length=255, null=True, blank=True)  # Ubicación
    image = models.ImageField(upload_to='user_fish_images', null=True, blank=True, verbose_name="Foto del pez capturado")  # Foto

    class Meta:
        verbose_name = "Relación Usuario-Pez"
        verbose_name_plural = "Relaciones Usuario-Pez"

    def __str__(self):
        return f"{self.user.name} - {self.fish.name} - Capturado: {'Sí' if self.captured else 'No'}"