"""Import Django models."""
from django.db import models
from .base import Base
from .lector import Lector
from ..fields import VISIBILITY_CHOICES


class Workshop(Base):
    """Stores workshops."""

    name = models.CharField(max_length=127)
    desc = models.TextField()
    difficulty = models.CharField(max_length=127)
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
    capacity = models.PositiveIntegerField(default=12)
    lector = models.ForeignKey(Lector, related_name='workshops')

    def __str__(self):
        """Return name as string representation."""
        return self.name
