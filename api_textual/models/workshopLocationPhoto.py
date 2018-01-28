"""Import Django models."""
from api.models.photo import Photo

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .workshopLocation import WorkshopLocation


class WorkshopLocationPhoto(Photo):
    """Stores workshop location photos."""

    text = models.ForeignKey(
        WorkshopLocation,
        verbose_name=_("Workshop Location"),
        related_name='photos',
        on_delete=models.CASCADE,
    )
