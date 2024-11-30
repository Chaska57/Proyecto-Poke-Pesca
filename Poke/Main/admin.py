from django.contrib import admin
from .models import Distribution, Diet, Fish, User


@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description','scientific_name','image')  # Columnas visibles
    search_fields = ('name', 'scientific_name')                                             # Búsqueda por campos                             # Filtros en la barra lateral                                                        # Campos solo lectura

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # Mostrar columnas en la lista
    search_fields = ('name', 'description')      # Campo de búsqueda
