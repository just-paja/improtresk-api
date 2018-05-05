"""Year model."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.fields import format_relation_link
from api.models.base import Base


class Inhabitant(Base):
    """Stores inhabitants."""
    participant = models.ForeignKey(
        'api.Participant',
        related_name='inhabited_rooms',
        verbose_name=_('Participant'),
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        'Room',
        related_name='inhabitants',
        verbose_name=_('Room'),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s@%s" % (self.room, self.participant)

    def participant_link(self):
        return format_relation_link('api_participant', self.participant.id, self.participant)

    def room_link(self):
        return format_relation_link('api_roommates_room', self.room.id, self.room)
