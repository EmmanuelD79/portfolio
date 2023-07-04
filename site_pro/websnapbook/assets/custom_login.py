from django.contrib.auth.backends import BaseBackend
from ..models import Guest

class GuestBackend(BaseBackend):
    def authenticate(self, request, email=None):
        try:
            guest = Guest.objects.get(email=email)
            guest.is_guest = True
            guest.is_authenticated = True
            guest.save()
            return guest
        except Guest.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Guest.objects.get(pk=user_id)
        except Guest.DoesNotExist:
            return None
