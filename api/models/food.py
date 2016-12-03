"""Import Django models."""
from django.db import models
from .base import Base
from ..fields import VISIBILITY_CHOICES

FOOD_CHOICES = (
    (1, 'Soup'),
    (2, 'Main course'),
)


class Food(Base):
    """Stores food types."""

    name = models.CharField(max_length=127)
    course = models.PositiveIntegerField(choices=FOOD_CHOICES)
    price = models.PositiveIntegerField()
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
    date = models.DateField()
    capacity = models.PositiveIntegerField(default=12)
