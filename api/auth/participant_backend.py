from ..models import Participant


class ParticipantBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = Participant.objects.get(email=username)
        except Participant.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            Participant().set_password(password)
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            user = Participant.objects.get(pk=user_id)
        except Participant.DoesNotExist:
            return None
        return user
