from django.shortcuts import render, redirect
from .models import Fish, User ,UserFish
from django.shortcuts import get_object_or_404, render
from decimal import Decimal

TIER_ORDER = {
    'SS': 1,
    'S': 2,
    'A': 3,
    'B': 4,
    'C': 5
}

def Mainmenu(request):
    peces = Fish.objects.all()
    usuarios = User.objects.all()

    # Obtener el parámetro de ordenación de la solicitud GET (si existe)
    orden = request.GET.get('orden', 'nombre_asc')  # Por defecto se ordena por nombre ascendente

    if orden == 'nombre_asc':
        peces_ordenados = peces.order_by('name')
    elif orden == 'nombre_desc':
        peces_ordenados = peces.order_by('-name')
    elif orden == 'tier_asc':
        peces_ordenados = sorted(peces, key=lambda fish: TIER_ORDER.get(fish.tier, float('inf')))
    elif orden == 'tier_desc':
        peces_ordenados = sorted(peces, key=lambda fish: TIER_ORDER.get(fish.tier, float('inf')), reverse=True)
    else:
        peces_ordenados = peces  # Orden por defecto
    def preparar_datos(peces):
        fish_data = []
        for fish in peces:
            captured_by_users = []
            for user in usuarios:
                # Verificar si este usuario ha capturado este pez
                captured = UserFish.objects.filter(user=user, fish=fish).first()
                captured_by_users.append({
                    'user': user,
                    'captured': captured and captured.captured  # Capturado o no capturado
                })

            fish_data.append({
                'fish': fish,
                'captured_by_users': captured_by_users
            })
        return fish_data

    # Datos ordenados
    data = {
        'peces_nombre': preparar_datos(peces_ordenados),  # Usamos peces_ordenados aquí
        'usuarios': usuarios,
    }

    return render(request, 'index.html', data)

def detalle_pez(request, id):
    # Obtener el pez según el ID o realizar búsqueda
    pez = get_object_or_404(Fish, id=id)
    query = request.GET.get('search', '')

    if query:
        pez = Fish.objects.filter(name__icontains=query).first() or pez

    # Obtener peces aleatorios excluyendo el pez actual
    peces_aleatorios = Fish.objects.exclude(id=pez.id).order_by('?')[:2]

    # Obtener todos los usuarios
    usuarios = User.objects.all()

    # Diccionario de datos para la plantilla
    data = {
        'pez': pez,
        'peces_aleatorios': peces_aleatorios,
        'search_query': query,
        'usuarios': usuarios,
    }

    # Renderizar la plantilla con los datos
    return render(request, 'detalle-pez.html', data)

def capture_fish(request, fish_id, user_id):
      if request.method == "POST":
        captured = request.POST.get("captured") == "true"
        user = get_object_or_404(User, id=user_id)
        fish = get_object_or_404(Fish, id=fish_id)
        
        # Obtener o crear la relación entre el usuario y el pez
        user_fish, created = UserFish.objects.get_or_create(user=user, fish=fish)
        
        # Actualizar el estado de capturado
        user_fish.captured = captured

        # Obtener el tamaño y peso desde el formulario
        size = request.POST.get('size')
        weight = request.POST.get('weight')
        image = request.FILES.get('image')

        if size:
            user_fish.size = Decimal(size)  # Asegurarse de que se guarde como decimal
        if weight:
            # Convertir el peso a entero (en gramos), eliminando los decimales
            try:
                user_fish.weight = int(float(weight))  # Convierte a float primero y luego a entero
            except ValueError:
                user_fish.weight = None  # Si el valor no es un número válido, asigna None
        if image:  # Si hay imagen, actualízala
            user_fish.image = image  # Guardar la foto subida

        # Guardar la relación actualizada
        user_fish.save()

        # Redirigir a la vista para mostrar los cambios
        return redirect("user_fish_view", user_id=user.id)
    
def user_fish_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    fishes = Fish.objects.all()

    user_fishes = [
        {
            "fish": fish,
            "captured": UserFish.objects.filter(user=user, fish=fish).first()
        }
        for fish in fishes
    ]

    captured_count = sum(1 for data in user_fishes if data["captured"] and data["captured"].captured)

    return render(
        request,
        "user_fish_view.html",
        {
            "user": user,
            "user_fishes": user_fishes,
            "captured_count": captured_count,
            "total_count": len(user_fishes),
        },
    )

def user_fish_poke(request, user_id):
    user = get_object_or_404(User, id=user_id)
    fishes = Fish.objects.all()

    user_fishes = [
        {
            "fish": fish,
            "captured": UserFish.objects.filter(user=user, fish=fish).first()
        }
        for fish in fishes
    ]

    captured_count = sum(1 for data in user_fishes if data["captured"] and data["captured"].captured)

    # Manejo del parámetro de orden
    orden = request.GET.get('orden', 'nombre_asc')  # Valor por defecto

    if orden == 'peso_desc':
        # Ordenar por peso, de mayor a menor
        user_fishes.sort(key=lambda x: x['captured'].weight if x['captured'] and x['captured'].weight is not None else -float('inf'), reverse=True)
    elif orden == 'peso_asc':
        # Ordenar por peso, de menor a mayor
        user_fishes.sort(key=lambda x: x['captured'].weight if x['captured'] and x['captured'].weight is not None else float('inf'))
    elif orden == 'tamaño_desc':
        # Ordenar por tamaño, de mayor a menor
        user_fishes.sort(key=lambda x: x['captured'].size if x['captured'] and x['captured'].size is not None else -float('inf'), reverse=True)
    elif orden == 'tamaño_asc':
        # Ordenar por tamaño, de menor a mayor
        user_fishes.sort(key=lambda x: x['captured'].size if x['captured'] and x['captured'].size is not None else float('inf'))
    elif orden == 'nombre_asc':
        # Ordenar por nombre, A-Z
        user_fishes.sort(key=lambda x: x['fish'].name)
    elif orden == 'nombre_desc':
        # Ordenar por nombre, Z-A
        user_fishes.sort(key=lambda x: x['fish'].name, reverse=True)
    elif orden == 'tier_asc':
        # Ordenar por tier ascendente
        tier_order = {'SS': 1, 'S': 2, 'A': 3, 'B': 4, 'C': 5, 'D': 6}
        user_fishes.sort(key=lambda x: tier_order.get(x['fish'].tier, float('inf')))
    elif orden == 'tier_desc':
        # Ordenar por tier descendente
        tier_order = {'SS': 1, 'S': 2, 'A': 3, 'B': 4, 'C': 5, 'D': 6}
        user_fishes.sort(key=lambda x: tier_order.get(x['fish'].tier, float('inf')), reverse=True)

    return render(
        request,
        "user_pokedex.html",
        {
            "user": user,
            "user_fishes": user_fishes,
            "captured_count": captured_count,
            "total_count": len(user_fishes),
        },
    )