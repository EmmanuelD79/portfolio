from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Profil


@receiver(pre_save, sender=Profil)
def deleting_photo_on_update(sender, instance, **kwargs):
    if instance.pk:
        old_photo = Profil.objects.get(pk=instance.pk).photo
        new_photo = instance.photo
        if old_photo and old_photo.url != new_photo.url:
            old_photo.delete(save=False)


@receiver(pre_save, sender=Profil)
def deleting_banner_on_update(sender, instance, **kwargs):
    if instance.pk:
        old_banner = Profil.objects.get(pk=instance.pk).banner
        new_banner = instance.banner
        if old_banner and old_banner.url != new_banner.url:
            old_banner.delete(save=False)


@receiver(pre_save, sender=Profil)
def deleting_description_img_on_update(sender, instance, **kwargs):
    if instance.pk:
        old_description_img = Profil.objects.get(
            pk=instance.pk).description_img
        new_description_img = instance.description_img
        if old_description_img and old_description_img.url != new_description_img.url:
            old_description_img.delete(save=False)
