"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from api_textual.models.abstractStub import AbstractStub


class AccomodationDescription(AbstractStub):
    """Stores accomodation types."""

    accomodation = models.ForeignKey(
        'Accomodation',
        verbose_name=_('Accomodation'),
        related_name='descriptions',
        on_delete=models.CASCADE,
    )
