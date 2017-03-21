"""Import Django models."""

from api.models.base import Base

from django.db import models

from django.utils.translation import ugettext_lazy as _


class PollAnswer(Base):
    """Stores possible Poll answers."""

    text = models.CharField(
        max_length=255,
        verbose_name=_('Answer'),
    )
    performer = models.ForeignKey(
        'Performer',
        related_name='polls',
        blank=True,
        null=True,
    )
    poll = models.ForeignKey(
        'Poll',
        related_name='answers',
    )

    def __str__(self):
        return '%s (%s)' % (self.text, self.poll.question)

    def get_vote_count(self):
        return self.votes.count()

    get_vote_count.short_description = _('Vote count')
