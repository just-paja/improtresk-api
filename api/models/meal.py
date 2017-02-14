"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .capacityMixin import CapacityMixin
from .reservation import Reservation
from ..fields import VISIBILITY_CHOICES

FOOD_CHOICES = (
    (1, _('Soup')),
    (2, _('Main course')),
)


class Meal(CapacityMixin, Base):
    """Stores meal."""

    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    name = models.CharField(
        verbose_name=_("Name of meal"),
        help_text=_("eg. Friday lunch"),
        max_length=127,
    )
    course = models.PositiveIntegerField(
        verbose_name=_("Course"),
        choices=FOOD_CHOICES,
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price"),
    )
    date = models.DateField(
        verbose_name=_("Date"),
    )
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)

    def get_reservations_query(self):
        """
        Returns query path from reservation to self.
        """
        return Reservation.objects.filter(mealreservation__meal=self)

    def __str__(self):
        """Return name as string representation."""
        return self.name
