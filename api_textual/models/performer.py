"""Import Django models."""
from api.fields import VISIBILITY_CHOICES, VISIBILITY_PUBLIC

from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.models.base import Base


class Performer(Base):
    """Stores performer data."""

    class Meta:
        verbose_name = _("Performer")
        verbose_name_plural = _("Performers")

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    slug = models.SlugField(
        verbose_name=_("Identifier in URL"),
    )
    year = models.ForeignKey(
        'api.Year',
        verbose_name=_('Year'),
        related_name='performers',
        on_delete=models.CASCADE,
    )
    visibility = models.PositiveIntegerField(
        default=VISIBILITY_PUBLIC,
        choices=VISIBILITY_CHOICES,
    )
