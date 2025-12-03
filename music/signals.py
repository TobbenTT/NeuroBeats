import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Song

@receiver(post_delete, sender=Song)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Borra los archivos del sistema cuando se elimina la canción de la DB.
    """
    # 1. Borrar el Audio
    if instance.audio_file:
        if os.path.isfile(instance.audio_file.path):
            os.remove(instance.audio_file.path)
            print(f"🗑️ Archivo de audio eliminado: {instance.audio_file.name}")

    # 2. Borrar la Portada
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)
            print(f"🗑️ Imagen eliminada: {instance.cover_image.name}")