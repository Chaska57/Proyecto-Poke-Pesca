from django.shortcuts import render, redirect
from .models import Fish, User ,UserFish
from django.shortcuts import get_object_or_404, render
from decimal import Decimal
from .forms import UserProfileForm
from collections import OrderedDict
import os
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


TIER_ORDER = {
    'SS': 1,
    'S': 2,
    'A': 3,
    'B': 4,
    'C': 5,
    'D': 6

}

def index(request):
    peces = Fish.objects.all()
    usuarios = User.objects.all()

    # Contador total de peces
    total_peces = peces.count()

    # Contador de peces por cada tier (en orden específico SS, S, A, B, C)
    contador_tiers = {tier: peces.filter(tier=tier).count() for tier in TIER_ORDER if peces.filter(tier=tier).exists()}

    # Obtener el parámetro de ordenación de la solicitud GET (si existe)
    orden = request.GET.get('orden', 'nombre_asc')  # Por defecto se ordena por nombre ascendente

    if orden == 'nombre_asc':
        peces_ordenados = peces.order_by('name')
    elif orden == 'nombre_desc':
        peces_ordenados = peces.order_by('-name')
    elif orden == 'tier_asc':
        peces_ordenados = sorted(peces, key=lambda fish: TIER_ORDER.index(fish.tier) if fish.tier in TIER_ORDER else float('inf'))
    elif orden == 'tier_desc':
        peces_ordenados = sorted(peces, key=lambda fish: TIER_ORDER.index(fish.tier) if fish.tier in TIER_ORDER else float('inf'), reverse=True)
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
        'peces_nombre': preparar_datos(peces_ordenados),
        'usuarios': usuarios,
        'total_peces': total_peces,  # Total de peces
        'contador_tiers': contador_tiers,  # Contador por tier
    }

    return render(request, 'index.html', data)

def fish_detail(request, id):
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
    return render(request, 'fish_detail.html', data)

def user_pokedex(request, user_id):
    user = get_object_or_404(User, id=user_id)
    fishes = Fish.objects.all()

    # Filtro de captura
    captura = request.GET.get('capturados', '')  # "capturados", "no_capturados" o "" para todos
    if captura == 'capturados':
        user_fishes = [
            {
                "fish": fish,
                "captured": UserFish.objects.filter(user=user, fish=fish, captured=True).first()
            }
            for fish in fishes
        ]
    elif captura == 'no_capturados':
        user_fishes = [
            {
                "fish": fish,
                "captured": UserFish.objects.filter(user=user, fish=fish, captured=False).first()
            }
            for fish in fishes
        ]
    else:
        # Si no se filtra por captura, se muestran todos los peces
        user_fishes = [
            {
                "fish": fish,
                "captured": UserFish.objects.filter(user=user, fish=fish).first()
            }
            for fish in fishes
        ]



    # Contar los peces capturados
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


    peces_capturados = [data["fish"] for data in user_fishes if data["captured"] and data["captured"].captured]


        # Crear un diccionario para contar los peces por tier, incluyendo aquellos con conteo 0, y mantener el orden
    contador_tiers = OrderedDict({
        tier: len([fish for fish in peces_capturados if fish.tier == tier])
        for tier in TIER_ORDER  # Asegura que todos los tiers estén en el diccionario y en el orden correcto
    })

    # Si un tier no tiene peces, su valor será 0
    for tier in TIER_ORDER:
        if tier not in contador_tiers:
            contador_tiers[tier] = 0

    return render(
        request,
        "user_pokedex.html",
        {
            "user": user,
            "user_fishes": user_fishes,
            "captured_count": captured_count,
            "total_count": len(user_fishes),
            "contador_tiers": contador_tiers,  # Contador por tier


        },
    )

def user_fish_detail(request, fish_id, user_id):

    user = get_object_or_404(User, id=user_id)
    fish = get_object_or_404(Fish, id=fish_id)
    user_fish, created = UserFish.objects.get_or_create(user=user, fish=fish)

   
    return render(
        request,
        "user_fish_detail.html",
        {
            "user": user,
            "user_fish": user_fish,
            
        },
    )

def edit_user_fish(request,user_id, fish_id):
    user = get_object_or_404(User, id=user_id)
    fish = get_object_or_404(Fish, id=fish_id)
    user_fish, created = UserFish.objects.get_or_create(user=user, fish=fish)

    if request.method == "POST":
        captured = request.POST.get("captured") == "true"
        user_fish.captured = captured

        # Actualizar los datos para el pez más grande
        biggest_fish_photo = request.FILES.get("biggest_fish_photo")
        biggest_fish_weight = request.POST.get("biggest_fish_weight")
        biggest_fish_size = request.POST.get("biggest_fish_size")
        biggest_fish_rod = request.POST.get("biggest_fish_rod")
        biggest_fish_reel = request.POST.get("biggest_fish_reel")
        biggest_fish_lure = request.POST.get("biggest_fish_lure")
        biggest_fish_location = request.POST.get("biggest_fish_location")

        if request.POST.get('delete_biggest_fish_photo'):
            user_fish.biggest_fish_photo = None  # Ruta de la foto de stock
            
        if request.POST.get('delete_biggest_fish_weight'):
            user_fish.biggest_fish_weight = None
            user_fish.save()  # Elimina el peso del pez más bonito

        if request.POST.get('delete_biggest_fish_size'):
            user_fish.biggest_fish_size = None
            user_fish.save()  # Elimina el tamaño del pez más bonito

        if request.POST.get('delete_biggest_fish_rod'):
            user_fish.biggest_fish_rod = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_biggest_fish_reel'):
            user_fish.biggest_fish_reel = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_biggest_fish_lure'):
            user_fish.biggest_fish_lure = None
            user_fish.save()  # Elimina el señuelo utilizado para el pez más bonito

        if request.POST.get('delete_biggest_fish_location'):
            user_fish.biggest_fish_location = None
            user_fish.save()  # Elimina la ubicación del pez más bonito

        if biggest_fish_weight:
            user_fish.biggest_fish_weight = int(biggest_fish_weight)
        if biggest_fish_size:
            user_fish.biggest_fish_size = Decimal(biggest_fish_size)
        if biggest_fish_rod:
            user_fish.biggest_fish_rod = biggest_fish_rod
        if biggest_fish_reel:
            user_fish.biggest_fish_reel = biggest_fish_reel
        if biggest_fish_lure:
            user_fish.biggest_fish_lure = biggest_fish_lure
        if biggest_fish_location:
            user_fish.biggest_fish_location = biggest_fish_location
        if biggest_fish_photo:
            user_fish.biggest_fish_photo = biggest_fish_photo

        # Actualizar los datos para el pez más chico
        smallest_fish_photo = request.FILES.get("smallest_fish_photo")
        smallest_fish_weight = request.POST.get("smallest_fish_weight")
        smallest_fish_size = request.POST.get("smallest_fish_size")
        smallest_fish_rod = request.POST.get("smallest_fish_rod")
        smallest_fish_reel = request.POST.get("smallest_fish_reel")
        smallest_fish_lure = request.POST.get("smallest_fish_lure")
        smallest_fish_location = request.POST.get("smallest_fish_location")

        if request.POST.get('delete_smallest_fish_photo'):
            user_fish.smallest_fish_photo = None  # Ruta de la foto de stock
           

        if request.POST.get('delete_smallest_fish_weight'):
            user_fish.smallest_fish_weight = None
            user_fish.save()  # Elimina el peso del pez más bonito

        if request.POST.get('delete_smallest_fish_size'):
            user_fish.smallest_fish_size = None
            user_fish.save()  # Elimina el tamaño del pez más bonito

        if request.POST.get('delete_smallest_fish_rod'):
            user_fish.biggest_fish_rod = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_smallest_fish_reel'):
            user_fish.biggest_fish_reel = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_smallest_fish_lure'):
            user_fish.smallest_fish_lure = None
            user_fish.save()  # Elimina el señuelo utilizado para el pez más bonito

        if request.POST.get('delete_smallest_fish_location'):
            user_fish.smallest_fish_location = None
            user_fish.save()  # Elimina la ubicación del pez más bonito

        if smallest_fish_weight:
            user_fish.smallest_fish_weight = int(smallest_fish_weight)
        if smallest_fish_size:
            user_fish.smallest_fish_size = Decimal(smallest_fish_size)
        if smallest_fish_rod:
            user_fish.smallest_fish_rod = smallest_fish_rod
        if smallest_fish_reel:
            user_fish.smallest_fish_reel = smallest_fish_reel
        if smallest_fish_lure:
            user_fish.smallest_fish_lure = smallest_fish_lure
        if smallest_fish_location:
            user_fish.smallest_fish_location = smallest_fish_location
        if smallest_fish_photo:
            user_fish.smallest_fish_photo = smallest_fish_photo


        # Actualizar los datos para el pez más bonito
        prettiest_fish_photo = request.FILES.get("prettiest_fish_photo")
        prettiest_fish_weight = request.POST.get("prettiest_fish_weight")
        prettiest_fish_size = request.POST.get("prettiest_fish_size")
        prettiest_fish_rod = request.POST.get("prettiest_fish_rod")
        prettiest_fish_reel = request.POST.get("prettiest_fish_reel")
        prettiest_fish_lure = request.POST.get("prettiest_fish_lure")
        prettiest_fish_location = request.POST.get("prettiest_fish_location")
        
        
        if request.POST.get('delete_prettiest_fish_photo'):
            user_fish.prettiest_fish_photo = None
              # Elimina la foto más bonita

        if request.POST.get('delete_prettiest_fish_weight'):
            user_fish.prettiest_fish_weight = None
            user_fish.save()  # Elimina el peso del pez más bonito

        if request.POST.get('delete_prettiest_fish_size'):
            user_fish.prettiest_fish_size = None
            user_fish.save()  # Elimina el tamaño del pez más bonito

        if request.POST.get('delete_prettiest_fish_rod'):
            user_fish.prettiest_fish_rod = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito
        
        if request.POST.get('delete_prettiest_fish_reel'):
            user_fish.prettiest_fish_reel = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_prettiest_fish_lure'):
            user_fish.prettiest_fish_lure = None
            user_fish.save()  # Elimina el señuelo utilizado para el pez más bonito

        if request.POST.get('delete_prettiest_fish_location'):
            user_fish.prettiest_fish_location = None
            user_fish.save()  # Elimina la ubicación del pez más bonito
        
        
        

        if prettiest_fish_weight:
            user_fish.prettiest_fish_weight = int(prettiest_fish_weight)
        if prettiest_fish_size:
            user_fish.prettiest_fish_size = Decimal(prettiest_fish_size)
        if prettiest_fish_rod:
            user_fish.prettiest_fish_rod = prettiest_fish_rod
        if prettiest_fish_reel:
            user_fish.prettiest_fish_reel = prettiest_fish_reel
        if prettiest_fish_lure:
            user_fish.prettiest_fish_lure = prettiest_fish_lure
        if prettiest_fish_location:
            user_fish.prettiest_fish_location = prettiest_fish_location
        if prettiest_fish_photo:
            user_fish.prettiest_fish_photo = prettiest_fish_photo

        # Guardar los cambios
        user_fish.save()

        # Redirigir a la vista de usuario-pez
        return redirect("edit_user_fish", user_id=user.id, fish_id=fish.id)

    return render(request, 'edit_fish.html', {'fish_data': user_fish})

def edit_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit_user_profile', user_id=user.id)  # Redirige al perfil del usuario
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})

def info(request):
    return render(request, 'informacion.html')


def copy(request,user_id, fish_id):
    user = get_object_or_404(User, id=user_id)
    fish = get_object_or_404(Fish, id=fish_id)
    user_fish, created = UserFish.objects.get_or_create(user=user, fish=fish)

    if request.method == "POST":
        captured = request.POST.get("captured") == "true"
        user_fish.captured = captured

        # Actualizar los datos para el pez más grande
        biggest_fish_photo = request.FILES.get("biggest_fish_photo")
        biggest_fish_weight = request.POST.get("biggest_fish_weight")
        biggest_fish_size = request.POST.get("biggest_fish_size")
        biggest_fish_equipment = request.POST.get("biggest_fish_equipment")
        biggest_fish_lure = request.POST.get("biggest_fish_lure")
        biggest_fish_location = request.POST.get("biggest_fish_location")

        if request.POST.get('delete_biggest_fish_photo'):
            user_fish.biggest_fish_photo = None  # Ruta de la foto de stock
            
        if request.POST.get('delete_biggest_fish_weight'):
            user_fish.biggest_fish_weight = None
            user_fish.save()  # Elimina el peso del pez más bonito

        if request.POST.get('delete_biggest_fish_size'):
            user_fish.biggest_fish_size = None
            user_fish.save()  # Elimina el tamaño del pez más bonito

        if request.POST.get('delete_biggest_fish_equipment'):
            user_fish.biggest_fish_equipment = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_biggest_fish_lure'):
            user_fish.biggest_fish_lure = None
            user_fish.save()  # Elimina el señuelo utilizado para el pez más bonito

        if request.POST.get('delete_biggest_fish_location'):
            user_fish.biggest_fish_location = None
            user_fish.save()  # Elimina la ubicación del pez más bonito

        if biggest_fish_weight:
            user_fish.biggest_fish_weight = int(biggest_fish_weight)
        if biggest_fish_size:
            user_fish.biggest_fish_size = Decimal(biggest_fish_size)
        if biggest_fish_equipment:
            user_fish.biggest_fish_equipment = biggest_fish_equipment
        if biggest_fish_lure:
            user_fish.biggest_fish_lure = biggest_fish_lure
        if biggest_fish_location:
            user_fish.biggest_fish_location = biggest_fish_location
        if biggest_fish_photo:
            user_fish.biggest_fish_photo = biggest_fish_photo

        # Actualizar los datos para el pez más chico
        smallest_fish_photo = request.FILES.get("smallest_fish_photo")
        smallest_fish_weight = request.POST.get("smallest_fish_weight")
        smallest_fish_size = request.POST.get("smallest_fish_size")
        smallest_fish_equipment = request.POST.get("smallest_fish_equipment")
        smallest_fish_lure = request.POST.get("smallest_fish_lure")
        smallest_fish_location = request.POST.get("smallest_fish_location")

        if request.POST.get('delete_smallest_fish_photo'):
            user_fish.smallest_fish_photo = None  # Ruta de la foto de stock
           

        if request.POST.get('delete_smallest_fish_weight'):
            user_fish.smallest_fish_weight = None
            user_fish.save()  # Elimina el peso del pez más bonito

        if request.POST.get('delete_smallest_fish_size'):
            user_fish.smallest_fish_size = None
            user_fish.save()  # Elimina el tamaño del pez más bonito

        if request.POST.get('delete_smallest_fish_equipment'):
            user_fish.smallest_fish_equipment = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_smallest_fish_lure'):
            user_fish.smallest_fish_lure = None
            user_fish.save()  # Elimina el señuelo utilizado para el pez más bonito

        if request.POST.get('delete_smallest_fish_location'):
            user_fish.smallest_fish_location = None
            user_fish.save()  # Elimina la ubicación del pez más bonito

        if smallest_fish_weight:
            user_fish.smallest_fish_weight = int(smallest_fish_weight)
        if smallest_fish_size:
            user_fish.smallest_fish_size = Decimal(smallest_fish_size)
        if smallest_fish_equipment:
            user_fish.smallest_fish_equipment = smallest_fish_equipment
        if smallest_fish_lure:
            user_fish.smallest_fish_lure = smallest_fish_lure
        if smallest_fish_location:
            user_fish.smallest_fish_location = smallest_fish_location
        if smallest_fish_photo:
            user_fish.smallest_fish_photo = smallest_fish_photo


        # Actualizar los datos para el pez más bonito
        prettiest_fish_photo = request.FILES.get("prettiest_fish_photo")
        prettiest_fish_weight = request.POST.get("prettiest_fish_weight")
        prettiest_fish_size = request.POST.get("prettiest_fish_size")
        prettiest_fish_equipment = request.POST.get("prettiest_fish_equipment")
        prettiest_fish_lure = request.POST.get("prettiest_fish_lure")
        prettiest_fish_location = request.POST.get("prettiest_fish_location")
        
        
        if request.POST.get('delete_prettiest_fish_photo'):
            user_fish.prettiest_fish_photo = None
              # Elimina la foto más bonita

        if request.POST.get('delete_prettiest_fish_weight'):
            user_fish.prettiest_fish_weight = None
            user_fish.save()  # Elimina el peso del pez más bonito

        if request.POST.get('delete_prettiest_fish_size'):
            user_fish.prettiest_fish_size = None
            user_fish.save()  # Elimina el tamaño del pez más bonito

        if request.POST.get('delete_prettiest_fish_equipment'):
            user_fish.prettiest_fish_equipment = None
            user_fish.save()  # Elimina el equipo utilizado para el pez más bonito

        if request.POST.get('delete_prettiest_fish_lure'):
            user_fish.prettiest_fish_lure = None
            user_fish.save()  # Elimina el señuelo utilizado para el pez más bonito

        if request.POST.get('delete_prettiest_fish_location'):
            user_fish.prettiest_fish_location = None
            user_fish.save()  # Elimina la ubicación del pez más bonito
        
        
        

        if prettiest_fish_weight:
            user_fish.prettiest_fish_weight = int(prettiest_fish_weight)
        if prettiest_fish_size:
            user_fish.prettiest_fish_size = Decimal(prettiest_fish_size)
        if prettiest_fish_equipment:
            user_fish.prettiest_fish_equipment = prettiest_fish_equipment
        if prettiest_fish_lure:
            user_fish.prettiest_fish_lure = prettiest_fish_lure
        if prettiest_fish_location:
            user_fish.prettiest_fish_location = prettiest_fish_location
        if prettiest_fish_photo:
            user_fish.prettiest_fish_photo = prettiest_fish_photo


        # Guardar los cambios
        user_fish.save()

       

        # Redirigir a la vista de usuario-pez
        return redirect("copy", user_id=user.id, fish_id=fish.id)

    return render(request, 'copy.html', {'fish_data': user_fish})












