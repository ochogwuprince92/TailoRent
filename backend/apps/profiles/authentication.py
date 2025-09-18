# profiles/authentication.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate a user by email OR phone_number, plus password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to fetch by email first (case-insensitive)
        user = None
        if username is None or password is None:
            return None

        # Attempt lookup by email
        try:
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            # If not found by email, try phone_number
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None

        # Check password and whether the user is active
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
