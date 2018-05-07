from django.http import Http404
from django.contrib.auth.models import User
from functools import wraps

from ..models import Order, Participant, Year


def require_participant(func):
    @wraps(func)
    def require_participant_wrapper(self, request, *args, **kwargs):
        try:
            self.participant = request.user.participant
        except (User.DoesNotExist, Participant.DoesNotExist):
            raise Http404
        return func(self, request, *args, **kwargs)
    return require_participant_wrapper


def require_year_active(func):
    @wraps(func)
    def require_year_active_wrapper(self, request, *args, **kwargs):
        try:
            self.year = Year.objects.filter_current().get()
        except (Year.DoesNotExist):
            raise Http404
        return func(self, request, *args, **kwargs)
    return require_year_active_wrapper


def require_order_active(func):
    @wraps(func)
    def require_order_active_wrapper(self, request, *args, **kwargs):
        try:
            self.order = Order.objects.filter_by_participant(
                self.participant,
                self.year
            ).get()
        except (Year.DoesNotExist):
            raise Http404
        return func(self, request, *args, **kwargs)
    return require_order_active_wrapper
