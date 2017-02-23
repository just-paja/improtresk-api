"""Import Django models."""
from api.models.photo import Photo

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .performer import Performer


class PerformerPhoto(Photo):
    """Stores performer photos."""

    text = models.ForeignKey(
        Performer,
        verbose_name=_("Performer"),
        related_name='photos',
    )
