from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('email')
        if not email or not password:
            return None
        try:
            user = User.objects.get(Q(email__iexact=email) | Q(username__iexact=email))
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
