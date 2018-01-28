"""Import Django models."""
from api.models.photo import Photo

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .news import News


class NewsPhoto(Photo):
    """Stores text photos."""

    text = models.ForeignKey(
        News,
        verbose_name=_("News"),
        related_name='photos',
        on_delete=models.CASCADE,
    )
