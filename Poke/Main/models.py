from django.db import models
from PIL import Image
from django.contrib.auth.models import User


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
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, verbose_name="Distribución")
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, verbose_name="Alimentación")
    average_size = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Talla Promedio (cm)")
    conservation_status = models.CharField(
        max_length=50, 
        choices=[
            ('LC', 'Menor Preocupación'),
            ('NT', 'Casi Amenazado'),
            ('VU', 'Vulnerable'),
            ('EN', 'En Peligro'),
            ('CR', 'En Peligro Crítico'),
            ('EW', 'Extinto en Estado Silvestre'),
            ('EX', 'Extinto')
        ],
        verbose_name="Estado de Conservación")

    sexual_dimorphism = models.CharField(
        max_length=50, 
        choices=[
            ('Si','Si'),
            ('No','No'),
            
        ],
        verbose_name="Dismofirmo sexual")
    fishing_season = models.CharField(max_length=255, verbose_name="Estación de Temporada de Pesca")
    fishing_bans = models.CharField(max_length=500, verbose_name="Vedas")
    water_temperature = models.CharField(max_length=100, verbose_name="Temperatura del Agua que Habita")
    image = models.ImageField(upload_to='fish_images', null=True, blank=True, verbose_name="Imagen del Pez")
    
    class Meta:
        verbose_name = "Pez"
        verbose_name_plural = "Peces"

    def save(self, *args, **kwargs):
        # Redimensionar la imagen antes de guardarla
        if self.image:
            img = Image.open(self.image)
            img = img.resize((500, 500))  # Cambiar el tamaño a 800x800 píxeles
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

class UserFish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, verbose_name="Pez")
    captured = models.BooleanField(default=False, verbose_name="Capturado")
    size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Tamaño (cm)")  # Tamaño en cm
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")  # Peso en kg
    image = models.ImageField(upload_to='user_fish_images', null=True, blank=True, verbose_name="Foto del pez capturado")  # Nueva foto


    class Meta:
        verbose_name = "Relación Usuario-Pez"
        verbose_name_plural = "Relaciones Usuario-Pez"

    def __str__(self):
        return f"{self.user.name} - {self.fish.name} - Capturado: {'Sí' if self.captured else 'No'}"