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
from music.views import home, upload_song, rate_song, delete_song, toggle_favorite, song_detail, search
from users.views import profile, edit_profile, create_user_fast, sign_out, public_profile, toggle_follow, admin_dashboard, admin_user_detail, admin_edit_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # Rutas de Música
    path('upload/', upload_song, name='upload'),
    path('song/<int:song_id>/', song_detail, name='song_detail'),
    path('search/', search, name='search'),
    path('rate/<int:song_id>/<int:score>/', rate_song, name='rate_song'),
    path('delete/<int:song_id>/', delete_song, name='delete_song'),
    path('favorite/<int:song_id>/', toggle_favorite, name='toggle_favorite'),
    
    # Rutas de Usuario
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('u/<str:username>/', public_profile, name='public_profile'),
    path('follow/<int:user_id>/', toggle_follow, name='toggle_follow'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/profile/'), name='change_password'),
    
    # God Mode
    path('god-mode/create-user/', create_user_fast, name='create_user_fast'),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', sign_out, name='logout'),

    # --- ZONA DE ADMINISTRACIÓN (TOBBEN) ---
    path('god-mode/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('god-mode/inspect/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
    path('god-mode/edit/<int:user_id>/', admin_edit_user, name='admin_edit_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)