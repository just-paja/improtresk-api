"""Import Django models."""
from django.db import models
from .base import Base
from ..fields import VISIBILITY_CHOICES


class Accomodation(Base):
    """Stores accomodation types."""

    name = models.CharField(max_length=127)
    desc = models.TextField()
    price = models.PositiveIntegerField()
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
    capacity = models.PositiveIntegerField(default=12)

    def __str__(self):
        """Return name as string representation."""
        return self.name
