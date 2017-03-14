"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .capacityMixin import CapacityMixin
from .meal import Meal
from .reservation import Reservation
from ..fields import VISIBILITY_CHOICES, VISIBILITY_PUBLIC

FOOD_CHOICES = (
    (1, 'Soup'),
    (2, 'Main course'),
)


class AbstractFood(CapacityMixin, Base):
    """Stores food types."""

    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("eg. Fish and chips"),
        max_length=127,
    )
    meal = models.ForeignKey(
        Meal,
        verbose_name=_("Meal"),
    )
    visibility = models.PositiveIntegerField(
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
    )

    def get_reservations_query(self):
        """
        Returns query path from reservation to self.
        """
        return Reservation.objects.filter(mealreservation__food=self)

    def __str__(self):
        """Return name as string representation."""
        return self.name


class Food(AbstractFood):
    pass


class Soup(AbstractFood):
    pass
