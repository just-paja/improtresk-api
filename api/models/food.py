"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .meal import Meal
from ..fields import VISIBILITY_CHOICES

FOOD_CHOICES = (
    (1, 'Soup'),
    (2, 'Main course'),
)


class Food(Base):
    """Stores food types."""

    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("eg. Fish and chips"),
        max_length=127,
    )
    capacity = models.PositiveIntegerField(
        verbose_name=_("Capacity"),
        default=None,
        null=True,
        blank=True,
    )
    meal = models.ForeignKey(
        Meal,
        verbose_name=_("Meal"),
    )
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)

    def __str__(self):
        """Return name as string representation."""
        return self.name
