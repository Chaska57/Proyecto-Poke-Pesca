from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('fish_detail/<int:id>/', views. fish_detail),
    path("user/<int:user_id>/", views.user_pokedex,name="use_pokedex"),
    path('fish_detail/<int:user_id>/<int:fish_id>/', views.user_fish_detail, name='user_fish_detail'),
    path("edit_user_fish/<int:user_id>/<int:fish_id>/", views.edit_user_fish, name="edit_user_fish"),
    path("edit_user_profile/<int:user_id>/", views.edit_user_profile, name="edit_user_profile"),
    path('info', views.info),
    path('copy/<int:user_id>/<int:fish_id>/', views.copy,name='copy'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)