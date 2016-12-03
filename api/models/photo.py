"""Import Django models."""
from django.db import models
from ..fields import VISIBILITY_CHOICES
from .base import Base


class Photo(Base):
    """Stores photos."""

    class Meta:
        """Defines photo as abstract class."""

        abstract = True

    image = models.ImageField(upload_to='var/photos')
    desc = models.CharField(max_length=255)
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
