from django.shortcuts import render, redirect
from .models import Fish, User ,UserFish
from django.shortcuts import get_object_or_404, render
from decimal import Decimal

def Mainmenu(request):

    peces = Fish.objects.all()
    usuarios = User.objects.all()

    peces_ordenados_nombre = peces.order_by('name')  # Orden alfabético
    peces_ordenados_nombre_inverso = peces.order_by('-name')  # Orden alfabético inverso
    peces_ordenados_tier = peces.order_by('tier__name')  

     # Obtener la captura de cada pez para todos los usuarios
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

    data = {
        'peces': fish_data,  # Usamos fish_data en lugar de peces
        'usuarios': usuarios
        
    }
    

    return render(request,'index.html',data)

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


def combined_view(request):
    users = User.objects.all()
    fishes = Fish.objects.all()

    user_fishes = {
        user: {
            "info": user,
            "fish": [
                {
                    "fish": fish,
                    "captured": UserFish.objects.filter(user=user, fish=fish).first()
                }
                for fish in fishes
            ],
            "captured_count": sum(
                1 for fish_data in [
                    {
                        "fish": fish,
                        "captured": UserFish.objects.filter(user=user, fish=fish).first()
                    }
                    for fish in fishes
                ] if fish_data["captured"] and fish_data["captured"].captured
            ),  # Cuenta los peces capturados
            "total_count": len(fishes)  # Total de peces disponibles
        }
        for user in users
    }

    return render(request, "combined_view.html", {"user_fishes": user_fishes})


def capture_fish(request, fish_id, user_id):
    if request.method == "POST":
        captured = request.POST.get("captured") == "true"
        user = get_object_or_404(User, id=user_id)
        fish = get_object_or_404(Fish, id=fish_id)
        
        # Obtener o crear la relación entre el usuario y el pez
        user_fish, created = UserFish.objects.get_or_create(user=user, fish=fish)
        
        # Actualizar el estado de capturado
        user_fish.captured = captured

        # Obtener el tamaño y peso desde el formulario y convertirlos a decimales
        size = request.POST.get('size')
        weight = request.POST.get('weight')
        image = request.FILES.get('image')

        if size:
            user_fish.size = Decimal(size)  # Asegurarse de que se guarde como decimal
        if weight:
            user_fish.weight = Decimal(weight)  # Asegurarse de que se guarde como decimal
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



