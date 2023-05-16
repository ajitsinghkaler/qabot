from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class Auth0Backend(BaseBackend):

    def authenticate(self, request, payload=None):
        if payload is None:
            return None

        username = payload.get('sub').replace('|', '.')
        if not username:
            return None

        user, _ = User.objects.get_or_create(username=username)
        # You can add additional user attributes from the payload here, e.g.,
        # user.email = payload.get('email', '')
        # user.first_name = payload.get('given_name', '')
        # user.last_name = payload.get('family_name', '')

        user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
