import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token


def generate_user_token(user) -> Token:
    token, _ = Token.objects.get_or_create(user=user)
    expiry_date = token.created + datetime.timedelta(seconds=1800)

    if expiry_date < timezone.now():
        token.delete()
        token = Token.objects.create(user=token.user)

    return token
