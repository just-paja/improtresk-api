"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from ..fields import VISIBILITY_CHOICES


class Photo(Base):
    """Stores photos."""

    class Meta:
        """Defines photo as abstract class."""

        abstract = True

    image = models.ImageField(upload_to='var/photos')
    desc = models.CharField(
        verbose_name=_("Description"),
        max_length=255,
        null=True,
        blank=True,
    )
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
