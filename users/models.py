from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image  # Necesario para la optimización
# Create your models here.

# 1 Modelo de insignias
class Badge(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripcion")
    icon_name = models.CharField(max_length=50, help_text="Nombre del icono CSS o archivo")
    criteria = models.CharField(max_length=100, help_text="Clave interna para la IA (ej: 'rock_lover')")

    def __str__(self):
        return self.name
    
# 2 Perfil Extendido
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografia")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', verbose_name="Avatar")

    # Relacion Many-ti-may con insignias

    badges = models.ManyToManyField(Badge, blank=True, related_name="owners")

    # Sistema de Seguidores
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

# --- NUEVO: PERFIL PRIVADO ---
    is_private = models.BooleanField(default=False, verbose_name="Perfil Privado")
    
    # Campo para rastrear la última actividad
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name="Última Actividad")

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # OPTIMIZACIÓN DE IMAGEN (PILLOW)
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                
                # 1. Si es muy grande, redimensionar
                if img.height > 800 or img.width > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size)
                    
                    # 2. Guardar optimizada
                    img.save(self.avatar.path, quality=70, optimize=True)
            except Exception as e:
                print(f"Error optimizando imagen: {e}")
                pass # Si falla, no rompemos nada, solo no se optimiza

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()