"""
URL configuration for Poke project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Mainmenu,name='mainmenu'),
    path('detalle/<int:id>/', views. detalle_pez),
    path("user/<int:user_id>/", views.user_fish_view, name="user_fish_view"),
    path("capture/<int:fish_id>/<int:user_id>/", views.capture_fish, name="capture_fish"),
    path("detalle/usuario/<int:user_id>/", views.user_fish_poke,name="user_fish_poke"),
    path('update/usuario/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('info', views.info),
    path('fish_detail/<int:user_id>/<int:fish_id>/', views.fish_detail, name='fish_detail'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)