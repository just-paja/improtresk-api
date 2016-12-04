"""Import Django models."""
from django.db import models
from .base import Base


class Lector(Base):
    """Stores lectors."""

    name = models.CharField(max_length=127)
    about = models.TextField()

    def __str__(self):
        """Return name as string representation."""
        return self.name
