from django.shortcuts import render

def Mainmenu(request):
    return render(request,'index.html')