"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views

# Importamos vistas de Musica y Usuarios
from music.views import home, upload_song, rate_song, delete_song, toggle_favorite
from users.views import profile, edit_profile, create_user_fast

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('upload/', upload_song, name='upload'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    # RUTA NUEVA PARA VOTAR: Recibe el ID de la canción y la nota (1-5)
    path('rate/<int:song_id>/<int:score>/', rate_song, name='rate_song'),
    path('delete/<int:song_id>/', delete_song, name='delete_song'),
    path('favorite/<int:song_id>/', toggle_favorite, name='toggle_favorite'),
    
    # 2. NUEVA RUTA PARA CAMBIAR CONTRASEÑA
    # Le decimos: "Usa la lógica de Django, pero mi HTML personalizado"
    path('password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/profile/' 
    ), name='change_password'),
    path('god-mode/create-user/', create_user_fast, name='create_user_fast'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)