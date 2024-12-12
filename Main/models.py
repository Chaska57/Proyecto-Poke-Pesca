from django.db import models
from PIL import Image, ExifTags
from django.contrib.auth.models import User
import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL.Image import Resampling
from django.core.files.storage import default_storage

def compress_and_crop_image(image, quality=85, target_width=500, target_height=500):
    # Abrir la imagen con Pillow
    img = Image.open(image)

    # Corregir la orientación basada en los metadatos EXIF
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif and orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # La imagen no tiene datos EXIF o no se pueden procesar
        pass

    # Convertir a modo RGB si es necesario
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Obtener dimensiones originales
    original_width, original_height = img.size
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height

    # Redimensionar para que la imagen cubra el área requerida
    if original_ratio > target_ratio:
        # La imagen es más ancha que el objetivo; ajustar altura y recortar ancho
        new_height = target_height
        new_width = int(new_height * original_ratio)
    else:
        # La imagen es más alta que el objetivo; ajustar ancho y recortar altura
        new_width = target_width
        new_height = int(new_width / original_ratio)

    # Redimensionar la imagen manteniendo el aspecto
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calcular el recorte para centrar la imagen
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    img = img.crop((left, top, right, bottom))

    # Guardar la imagen comprimida en un buffer
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    buffer.seek(0)

    # Retornar la imagen comprimida y recortada
    return ContentFile(buffer.read(), name=image.name)

def compress_and_crop_image_banner(image, quality=85, target_width=1280, target_height=427):
    # Abrir la imagen con Pillow
    img = Image.open(image)

    # Corregir la orientación basada en los metadatos EXIF
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif and orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # La imagen no tiene datos EXIF o no se pueden procesar
        pass

    # Convertir a modo RGB si es necesario
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Obtener dimensiones originales
    original_width, original_height = img.size
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height

    # Redimensionar para que la imagen cubra el área requerida
    if original_ratio > target_ratio:
        # La imagen es más ancha que el objetivo; ajustar altura y recortar ancho
        new_height = target_height
        new_width = int(new_height * original_ratio)
    else:
        # La imagen es más alta que el objetivo; ajustar ancho y recortar altura
        new_width = target_width
        new_height = int(new_width / original_ratio)

    # Redimensionar la imagen manteniendo el aspecto
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calcular el recorte para centrar la imagen
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    img = img.crop((left, top, right, bottom))

    # Guardar la imagen comprimida en un buffer
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    buffer.seek(0)

    # Retornar la imagen comprimida y recortada
    return ContentFile(buffer.read(), name=image.name)

def compress_and_crop_image_to_468x290(image, quality=85, target_width=468, target_height=290):
    # Abrir la imagen con Pillow
    img = Image.open(image)

    # Corregir la orientación basada en los metadatos EXIF
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif and orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # La imagen no tiene datos EXIF o no se pueden procesar
        pass

    # Convertir a modo RGB si es necesario
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Obtener dimensiones originales
    original_width, original_height = img.size
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height

    # Redimensionar para cubrir el área requerida sin cambiar la orientación
    if original_ratio > target_ratio:
        # La imagen es más ancha que el objetivo; ajustar altura y recortar ancho
        new_height = target_height
        new_width = int(new_height * original_ratio)
    else:
        # La imagen es más alta que el objetivo; ajustar ancho y recortar altura
        new_width = target_width
        new_height = int(new_width / original_ratio)

    # Redimensionar la imagen manteniendo el aspecto
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calcular el recorte para centrar la imagen
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    img = img.crop((left, top, right, bottom))

    # Guardar la imagen comprimida en un buffer
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    buffer.seek(0)

    # Retornar la imagen comprimida y recortada
    return ContentFile(buffer.read(), name=image.name)

class Fish(models.Model):

    def get_media_path_fish(self, filename):
            ruta = 'fish_images/'
            
            if ruta not in filename:
                filename = ruta + filename
            return filename 


    name = models.CharField(max_length=255, verbose_name="Nombre")
    scientific_name = models.CharField(max_length=255, verbose_name="Nombre Científico")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    image = models.ImageField(upload_to=get_media_path_fish, null=True, blank=True, verbose_name="Imagen del Pez")
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
        if self.image:
            self.image = compress_and_crop_image_to_468x290(self.image)
        
        super().save(*args, **kwargs)        

    def __str__(self):
        return self.name

class User(models.Model):

    def get_media_path(self, filename):
            ruta = 'user_photos/'
            
            if ruta not in filename:
                filename = ruta + filename
            return filename 

    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    photo = models.ImageField(upload_to=get_media_path, verbose_name="Foto del Usuario")
    fishes = models.ManyToManyField('Fish', through='UserFish', related_name='users', verbose_name="Peces Capturados")
    banner= models.ImageField(upload_to=get_media_path, verbose_name="Foto banner")
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Guarda una referencia a la imagen original cargada
        self._original_photo = self.photo
        self._original_banner = self.banner

   
    def save(self, *args, **kwargs):
        # Verifica si la foto actual es diferente de la original
        if self.photo and self.photo != self._original_photo:
            # Borra la foto anterior si existe
            if self._original_photo and default_storage.exists(self._original_photo.name):
                default_storage.delete(self._original_photo.name)

            # Comprime y recorta la nueva foto
            self.photo = compress_and_crop_image(self.photo)

        if self.banner and self.banner != self._original_banner:
            # Borra la foto anterior si existe
            if self._original_banner and default_storage.exists(self._original_banner.name):
                default_storage.delete(self._original_banner.name)

            # Comprime y recorta la nueva foto
            self.banner = compress_and_crop_image_banner(self.banner)

        super().save(*args, **kwargs)

class UserFish(models.Model):

    def get_media_path_userfish(self, filename):
                ruta = 'user_fish_images/'
                
                if ruta not in filename:
                    filename = ruta + filename
                return filename 

    # Campos base
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, verbose_name="Pez")
    captured = models.BooleanField(default=False, verbose_name="Capturado")
    
    biggest_fish_photo = models.ImageField(upload_to=get_media_path_userfish, null=True, blank=True, verbose_name="Foto del pez más grande")
    biggest_fish_weight = models.IntegerField(null=True, blank=True, verbose_name="Peso del pez más grande (gramos)")
    biggest_fish_size = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Tamaño del pez más grande (cm)")
    biggest_fish_rod = models.CharField(max_length=255, null=True, blank=True, verbose_name="Caña utilizado para el pez más grande")
    biggest_fish_reel = models.CharField(max_length=255, null=True, blank=True, verbose_name="Carrete utilizado para el pez más grande")
    biggest_fish_lure = models.CharField(max_length=255, null=True, blank=True, verbose_name="Señuelo utilizado para el pez más grande")
    biggest_fish_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación del pez más grande")

    # Campos para el pez más bonito
    prettiest_fish_photo = models.ImageField(upload_to=get_media_path_userfish, null=True, blank=True, verbose_name="Foto del pez más bonito")
    prettiest_fish_rod = models.CharField(max_length=255, null=True, blank=True, verbose_name="Caña utilizado para el pez más bonito")
    prettiest_fish_reel = models.CharField(max_length=255, null=True, blank=True, verbose_name="Carrete utilizado para el pez más bonito")
    prettiest_fish_lure = models.CharField(max_length=255, null=True, blank=True, verbose_name="Señuelo utilizado para el pez más bonito")
    prettiest_fish_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación del pez más bonito")
    prettiest_fish_weight = models.IntegerField(null=True, blank=True, verbose_name="Peso del pez más bonito (gramos)")
    prettiest_fish_size = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Tamaño del pez más bonito (cm)")
    
    # Campos para el pez más chico
    smallest_fish_photo = models.ImageField(upload_to=get_media_path_userfish, null=True, blank=True, verbose_name="Foto del pez más chico")
    smallest_fish_weight = models.IntegerField(null=True, blank=True, verbose_name="Peso del pez más chico (gramos)")
    smallest_fish_size = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Tamaño del pez más chico (cm)")
    smallest_fish_rod = models.CharField(max_length=255, null=True, blank=True, verbose_name="Caña utilizado para el pez más chico")
    smallest_fish_reel = models.CharField(max_length=255, null=True, blank=True, verbose_name="Carrete utilizado para el pez más chico")
    smallest_fish_lure = models.CharField(max_length=255, null=True, blank=True, verbose_name="Señuelo utilizado para el pez más chico")
    smallest_fish_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación del pez más chico")

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Guarda una referencia a la imagen original cargada
            self._original_biggest_fish_photo = self.biggest_fish_photo
            self._original_smallest_fish_photo = self.smallest_fish_photo
            self._original_prettiest_fish_photo = self.prettiest_fish_photo



    def save(self, *args, **kwargs):
        if self.biggest_fish_photo and self.biggest_fish_photo != self._original_biggest_fish_photo:
            # Borra la foto anterior si existe
            if self._original_biggest_fish_photo and default_storage.exists(self._original_biggest_fish_photo.name):
                default_storage.delete(self._original_biggest_fish_photo.name)
            
            # Comprime y recorta la nueva foto
            self.biggest_fish_photo = compress_and_crop_image_to_468x290(self.biggest_fish_photo)

        if self.prettiest_fish_photo and self.prettiest_fish_photo != self._original_prettiest_fish_photo:
                    # Borra la foto anterior si existe
                    if self._original_prettiest_fish_photo and default_storage.exists(self._original_prettiest_fish_photo.name):
                        default_storage.delete(self._original_prettiest_fish_photo.name)
                    
                    # Comprime y recorta la nueva foto
                    self.prettiest_fish_photo = compress_and_crop_image_to_468x290(self.prettiest_fish_photo)

        if self.smallest_fish_photo and self.smallest_fish_photo != self._original_smallest_fish_photo:
                    # Borra la foto anterior si existe
                    if self._original_smallest_fish_photo and default_storage.exists(self._original_smallest_fish_photo.name):
                        default_storage.delete(self._original_smallest_fish_photo.name)
                    
                    # Comprime y recorta la nueva foto
                    self.smallest_fish_photo = compress_and_crop_image_to_468x290(self.smallest_fish_photo)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Relación Usuario-Pez"
        verbose_name_plural = "Relaciones Usuario-Pez"

    def __str__(self):
        return f"{self.user.name} - {self.fish.name} - Capturado: {'Sí' if self.captured else 'No'}"
