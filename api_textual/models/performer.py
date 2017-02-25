"""Import Django models."""
from api.fields import VISIBILITY_CHOICES, VISIBILITY_PUBLIC

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText


class Performer(AbstractText):
    """Stores performer data."""

    year = models.ForeignKey(
        'api.Year',
        verbose_name=_('Year'),
        related_name='performers',
    )
    visibility = models.PositiveIntegerField(
        default=VISIBILITY_PUBLIC,
        choices=VISIBILITY_CHOICES,
    )

    class Meta:
        verbose_name = _("Performer")
        verbose_name_plural = _("Performers")
