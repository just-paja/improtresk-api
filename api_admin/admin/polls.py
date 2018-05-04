from api_textual import models as models_text

from ..models import BaseAdminModel, BaseInlineAdminModel, DEFAULT_READONLY


class PollAnswerInlineAdmin(BaseInlineAdminModel):
    """Inline admin for Poll Answers."""

    model = models_text.PollAnswer
    readonly_fields = ['get_vote_count']


class PollAdmin(BaseAdminModel):
    """Admin for Polls."""

    inlines = [
        PollAnswerInlineAdmin,
    ]
    list_display = (
        'question',
        'closed',
        'get_answer_count',
        'get_vote_count',
        'get_winning_answer',
        'get_last_vote_date',
        'updated_at',
    )
    readonly_fields = [
        'get_answer_count',
        'get_vote_count',
        'get_winning_answer',
        'get_last_vote_date',
    ] + DEFAULT_READONLY
