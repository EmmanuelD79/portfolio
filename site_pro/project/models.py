from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100, blank=False)
    sub_title = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=1500, blank=False)
    project_img = models.ImageField(
        upload_to='project/', blank=True, null=True, verbose_name='Photo du projet')
    project_url = models.URLField("Url", max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = 'Projet'

    def __str__(self):
        return self.title
