"""Import Django models."""

from api.models.base import Base

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Poll(Base):
    """Stores polls."""

    question = models.CharField(
        max_length=255,
        verbose_name=_('Poll question'),
        help_text=_('For example What is the capital of Czech republic'),
    )
    closed = models.BooleanField(
        default=False,
        verbose_name=_('Poll is closed'),
    )

    def __str__(self):
        append = _('Closed') if self.closed else _('Open')
        return '%s (%s)' % (self.question, append)

    def get_last_vote_date(self):
        return self.answers\
            .aggregate(max_date=models.Max('votes__created_at'))\
            .get('max_date', None)

    def get_winning_answer(self):
        return self.answers\
            .annotate(max_votes=models.Count('votes'))\
            .order_by('-max_votes')\
            .filter(max_votes__gt=0)\
            .first()

    def get_answer_count(self):
        return self.answers.count()

    def get_vote_count(self):
        return self.answers\
            .aggregate(votes=models.Count('votes'))\
            .get('votes', 0)

    get_answer_count.short_description = _('Answer Count')
    get_last_vote_date.short_description = _('Last vote date')
    get_vote_count.short_description = _('Vote Count')
    get_winning_answer.short_description = _('Winning answer')
