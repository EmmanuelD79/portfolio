from django.db import models
from profil.models import Profil
from django.template.defaultfilters import slugify

class Project(models.Model):
    user = models.ForeignKey(Profil, blank=False, verbose_name='Créateur du projet', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    sub_title = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=1500, blank=False)
    project_img = models.ImageField(
        upload_to='project/', blank=True, null=True, verbose_name='Photo du projet')
    project_url = models.URLField("Url", max_length=256, blank=True, null=True)
    project_slug = models.SlugField(max_length=200, verbose_name='Url de la page du projet')
    
    class Meta:
        verbose_name = 'Projet'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.project_slug:
            self.project_slug = slugify(self.title)
        return super().save(*args, **kwargs)