"""Year model."""
from api_textual.models import WorkshopLocation

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .workshop import Workshop
from ..fields import VISIBILITY_PUBLIC


class Year(Base):
    """Stores years."""

    year = models.SlugField(
        verbose_name=_("Year"),
        unique=True,
    )
    topic = models.TextField(
        verbose_name=_("Topic of this year"),
        null=False,
        blank=True,
    )
    start_date = models.DateField(
        verbose_name=_("Date of festival start"),
    )
    end_date = models.DateField(
        verbose_name=_("Date of festival end"),
    )
    start_date_of_signups = models.DateTimeField(
        verbose_name=_("Date and time when signups are starting"),
        null=True,
        blank=True,
    )
    current = models.BooleanField(
        verbose_name=_("Is this year current?"),
    )

    def __str__(self):
        """Return name as string representation."""
        return "Year %s" % self.year

    def get_workshops(self):
        return Workshop.objects.distinct().filter(
            prices__price_level__in=self.price_levels.all(),
            visibility=VISIBILITY_PUBLIC,
        )

    def get_locations(self):
        return WorkshopLocation.objects.distinct().filter(
            workshop__in=self.get_workshops(),
        )
