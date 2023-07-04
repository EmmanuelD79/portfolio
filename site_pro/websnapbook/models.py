from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
import datetime
from django.utils.deconstruct import deconstructible
import os

class Event(models.Model):
    name = models.CharField(max_length=100,)
    date = models.DateField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=50, null=True, blank=True)
    qrcode = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Evenement"
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class GuestManager(BaseUserManager):
    def create_user(self, email, username, token, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_guest', True)
        return self._create_user(email, username, token, **extra_fields)

    def create_superuser(self, email, username, token, **extra_fields):
        raise NotImplementedError('Cannot create superuser for Guest model.')

    def _create_user(self, email, username, token, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not token:
            raise ValueError('The Token field must be set')

        email = self.normalize_email(email)
        guest = self.model(email=email, username=username,
                           token=token, **extra_fields)
        guest.save(using=self._db)
        return guest


class Guest(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    events = models.ManyToManyField('Event', related_name='guests')
    
    password = None

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'token']

    objects = GuestManager()

    class Meta:
        verbose_name = "Invité"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False
    
    @staticmethod
    def authenticate_by_email(email):
        try:
            guest = Guest.objects.get(email=email)
            return guest
        except Guest.DoesNotExist:
            return None
        
    # @staticmethod
    # def get_user(user_id):
    #     try:
    #         return Guest.objects.get(pk=user_id)
    #     except Guest.DoesNotExist:
    #         return None

# def set_filename_format(now, instance, filename):
#     """
#     file format setting
#     e.g)
#         {username}-{date}-{microsecond}{extension}
#         hjh-2016-07-12-158859.png
#     """
#     return "{username}-{date}-{microsecond}{extension}".format(
#         username=instance.uploader.username,
#         date=str(now.date()),
#         microsecond=now.microsecond,
#         extension=os.path.splitext(filename)[1],
#     )



# def event_directory_path(instance, filename):
#     now = datetime.datetime.now()
#     filename=set_filename_format(now, instance, filename)
#     path = f"photos/{instance.event.token}/{file}"

#     return path


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,)
    uploader = models.ForeignKey(Guest, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True,)
    likes = models.ManyToManyField(
        User, related_name='liked_photos', blank=True)

    class Meta:
        verbose_name = "Photo"
        ordering = ('uploaded_at',)

    def __str__(self) -> str:
        return f'Photo uploaded by {self.uploader.username}'

    def toggle_like(self, user):
        """
        Toggle the like status for the given user.
        If the user has already liked the photo, remove the like.
        If the user has not liked the photo, add the like.
        """
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    commenter = models.ForeignKey(Guest, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        ordering = ('commented_at',)

    def __str__(self) -> str:
        return f'Comment by {self.commenter.username}'
