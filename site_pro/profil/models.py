from django.db import models


class Profil(models.Model):
    full_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to='profil/', blank=True, null=True, verbose_name="Photo de profil")
    banner = models.ImageField(upload_to='profil/', blank=True, null=True, verbose_name="Bannière")
    sub_title = models.CharField(max_length=80, blank=False)
    resume = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=1500, blank=False)
    description_url = models.URLField("Url", max_length=256, blank=True, null=True)
    description_img = models.ImageField(upload_to='profil/', blank=True, null=True, verbose_name="Description photo")
    footer_text = models.TextField(max_length=1500, blank=False)
     
     
    class Meta:
        verbose_name = 'profil'
        verbose_name_plural = 'profils'
        
    def __str__(self):
        return self.email
    
    
    
