"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText

CATEGORIES = [
    ('home', _('homepage')),
    ('accomodation', _('accomodation')),
    ('fees', _('fees')),
    ('food', _('food')),
    ('locations', _('locations')),
    ('schedule', _('schedule')),
]


class Text(AbstractText):
    """Stores Text."""

    category = models.CharField(
        verbose_name=_("Category"),
        max_length=127,
        choices=CATEGORIES,
        null=True,
    )

    class Meta:
        verbose_name = _("Text item")
        verbose_name_plural = _("Text items")
