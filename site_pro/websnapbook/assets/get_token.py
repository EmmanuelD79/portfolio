import secrets
from ..models import Guest

def generate_unique_token(myModel):
    while True:
        token = secrets.token_hex(16)
        if not myModel.objects.filter(token=token).exists():
            return token
