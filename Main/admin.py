from django.contrib import admin
from .models import Fish, User, UserFish


@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description','scientific_name','image')  # Columnas visibles
    search_fields = ('name', 'scientific_name')                                             # Búsqueda por campos                             # Filtros en la barra lateral                                                        # Campos solo lectura

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # Mostrar columnas en la lista
    search_fields = ('name', 'description')      # Campo de búsqueda

@admin.register(UserFish)
class UserFishAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del admin
    list_display = (
        'user', 
        'fish', 
        'captured'
    )
    # Campos que permiten buscar registros
    search_fields = ('user__username', 'fish__name')  # Corregir si "username" es el campo correcto
    # Campos para filtrar en la lista
    list_filter = ('captured',)  # Debe ser una tupla o lista (añadido `,` para convertirlo en una tupla)
    # Configuración para los campos que se editan directamente en la lista
    list_editable = ('captured',)
    # Configuración para mostrar más detalles en la vista de edición
    fieldsets = (
        ('Información General', {
            'fields': ('user', 'fish', 'captured')
        }),
        ('Pez Más Grande', {
            'fields': (
                'biggest_fish_photo', 
                'biggest_fish_weight', 
                'biggest_fish_size', 
                'biggest_fish_equipment', 
                'biggest_fish_lure', 
                'biggest_fish_location'
            )
        }),
        ('Pez Más Bonito', {
            'fields': (
                'prettiest_fish_photo', 
                'prettiest_fish_equipment', 
                'prettiest_fish_lure', 
                'prettiest_fish_location'
                'prettiest_fish_weight', 
                'prettiest_fish_size',
            )
        }),
        ('Pez Más Chico', {
            'fields': (
                'smallest_fish_photo', 
                'smallest_fish_weight', 
                'smallest_fish_size', 
                'smallest_fish_equipment', 
                'smallest_fish_lure', 
                'smallest_fish_location'
            )
        }),
    )
    # Mostrar las imágenes directamente en el admin
    readonly_fields = ('biggest_fish_photo', 'prettiest_fish_photo', 'smallest_fish_photo')