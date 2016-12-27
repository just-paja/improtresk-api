"""Import Django models."""
from api.models.photo import Photo

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .text import Text


class TextPhoto(Photo):
    """Stores text photos."""

    text = models.ForeignKey(
        Text,
        verbose_name=_("Text"),
        related_name='photos',
    )
