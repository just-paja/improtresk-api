"""Year model."""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.fields import format_relation_link
from api.models.base import Base


class Room(Base):
    """Stores rooms."""
    accomodation = models.ForeignKey(
        'api.Accomodation',
        related_name='rooms',
        on_delete=models.CASCADE,
    )
    number = models.CharField(
        verbose_name=_("Room Number"),
        max_length=255,
    )
    size = models.PositiveIntegerField(
        verbose_name=_('Size'),
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s %s" % (self.accomodation, self.number)

    def accomodation_link(self):
        return format_relation_link('api_accomodation', self.accomodation.id, self.accomodation)

    def remaining_capacity(self):
        return self.size - self.inhabitants.count()
