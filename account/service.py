from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    user.last_login = timezone.now()

    return refresh
