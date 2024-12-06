from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Mainmenu,name='mainmenu'),
    path('detalle/<int:id>/', views. detalle_pez),
    path("user/<int:user_id>/", views.user_poke_edit, name="user_poke_edit"),
    path("capture/<int:fish_id>/<int:user_id>/", views.update_capture_fish, name="update_capture_fish"),
    path("detalle/usuario/<int:user_id>/", views.user_poke,name="use_poke"),
    path('update/usuario/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('info', views.info),
    path('fish_detail/<int:user_id>/<int:fish_id>/', views.user_fish_detail, name='user_fish_detail'),
    path("capture/update_biggest/<int:fish_id>/<int:user_id>/", views.update_biggest, name="update_biggest"),
    path("capture/update_smallest/<int:fish_id>/<int:user_id>/", views.update_smallest, name="update_smallest"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)