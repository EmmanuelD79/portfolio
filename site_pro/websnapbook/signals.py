from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Photo, Event
import os


# @receiver(pre_save, sender=Photo)
# def set_event_token(sender, instance, **kwargs):
#     if not instance.pk:  # Vérifie si l'instance est nouvellement créée
#         event_token = instance.event.token
#         instance.image.upload_to = f"media/photos/{event_token}/"
        

# @receiver(pre_save, sender=Event)
# def create_event_directory(sender, instance, **kwargs):
#     if not instance.pk:
#         event_token = instance.token
#         directory_path = f'media/photos/{event_token}'
#         os.makedirs(directory_path, exist_ok=True)