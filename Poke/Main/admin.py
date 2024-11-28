from django.contrib import admin
from .models import Distribution, Diet, Fish, User

# Registrar los modelos en el panel de administración
@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')  # Mostrar columnas en la lista
    search_fields = ('description',)     # Campo de búsqueda

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('description',)

@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'scientific_name', 'conservation_status', 'average_size','image')  # Columnas visibles
    search_fields = ('name', 'scientific_name')                                             # Búsqueda por campos
    list_filter = ('conservation_status', 'fishing_season')                                 # Filtros en la barra lateral                                                        # Campos solo lectura

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # Mostrar columnas en la lista
    search_fields = ('name', 'description')      # Campo de búsqueda
