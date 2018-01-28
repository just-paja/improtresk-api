"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText


class News(AbstractText):
    """Stores news."""

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News list")

    poll = models.ForeignKey(
        'Poll',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
