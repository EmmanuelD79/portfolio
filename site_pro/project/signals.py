from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project


@receiver(pre_save, sender=Project)
def deleting_photo_on_update(sender, instance, **kwargs):
    if instance.pk:
        old_project_img = Project.objects.get(pk=instance.pk).project_img
        new_project_img = instance.project_img
        if old_project_img and old_project_img.url != new_project_img.url:
            old_project_img.delete(save=False)