"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstractStub import AbstractStub


class WorkshopLocationDescription(AbstractStub):
    """Stores workshop location."""

    class Meta:
        verbose_name = _("Workshop Location Description")
        verbose_name_plural = _("Workshop Location Descriptions")

    performer = models.ForeignKey(
        'WorkshopLocation',
        verbose_name=_('WorkshopLocation'),
        related_name='descriptions',
        on_delete=models.CASCADE,
    )
