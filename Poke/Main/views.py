from django.shortcuts import render
from .models import Fish, User

def Mainmenu(request):

    peces = Fish.objects.all()
    usuarios = User.objects.all()

    data ={
        'peces' : peces,
        'usuarios' : usuarios
    }

    return render(request,'index.html',data)