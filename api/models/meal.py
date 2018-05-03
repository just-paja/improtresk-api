"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .capacityMixin import CapacityMixin
from .reservation import Reservation
from .year import Year
from ..fields import VISIBILITY_CHOICES, VISIBILITY_PUBLIC

MEAL_NAME_CHOICES = (
    ('lunch', _('Lunch')),
    ('dinner', _('Dinner')),
)


class Meal(CapacityMixin, Base):
    """Stores meal and course, for example Friday lunch soup."""

    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    name = models.CharField(
        max_length=127,
        default='lunch',
        choices=MEAL_NAME_CHOICES,
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price"),
    )
    date = models.DateField(
        verbose_name=_("Date"),
    )
    visibility = models.PositiveIntegerField(
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
    )
    year = models.ForeignKey(
        Year,
        related_name="meals",
        on_delete=models.CASCADE,
    )

    def get_reservations_query(self):
        """
        Returns query path from reservation to self.
        """
        return Reservation.objects.filter(mealreservation__meal=self)

    def __str__(self):
        """Return name as string representation."""
        return "(%s) %s at %s" % (
            self.year.year,
            self.get_name_display(),
            self.date.strftime('%A')
        )
