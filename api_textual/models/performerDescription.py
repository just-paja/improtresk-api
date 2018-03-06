"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstractStub import AbstractStub


class PerformerDescription(AbstractStub):
    """Stores performer data."""

    class Meta:
        verbose_name = _("Performer Description")
        verbose_name_plural = _("Performer Descriptions")

    performer = models.ForeignKey(
        'Performer',
        verbose_name=_('Performer'),
        related_name='descriptions',
        on_delete=models.CASCADE,
    )
