"""Tests for participant model."""

from datetime import datetime

from api_textual.models import PollAnswer, PollVote

from django.test import TestCase

from model_mommy import mommy

import pytz


class PollTest(TestCase):

    def test_poll_text_representation_open(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
        )
        self.assertEquals(str(poll), 'Do you like dogs? (Open)')

    def test_poll_text_representation_closed(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
            closed=True,
        )
        self.assertEquals(str(poll), 'Do you like dogs? (Closed)')

    def test_get_answer_count(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
            answers=[
                mommy.make(
                    'api_textual.PollAnswer',
                    text='foo',
                ),
                mommy.make(
                    'api_textual.PollAnswer',
                    text='bar',
                ),
            ],
        )
        self.assertEquals(poll.get_answer_count(), 2)

    def test_get_vote_count(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
            answers=[
                mommy.make(
                    'api_textual.PollAnswer',
                    text='foo',
                    votes=[
                        mommy.make('api_textual.PollVote'),
                        mommy.make('api_textual.PollVote'),
                    ],
                ),
                mommy.make(
                    'api_textual.PollAnswer',
                    text='bar',
                    votes=[
                        mommy.make('api_textual.PollVote'),
                    ],
                ),
            ],
        )
        self.assertEquals(poll.get_vote_count(), 3)

    def test_get_last_vote_date(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
            answers=[
                mommy.make(
                    'api_textual.PollAnswer',
                    text='foo',
                    votes=[
                        mommy.make(
                            'api_textual.PollVote',
                            created_at='2016-01-02T13:15:16Z',
                        ),
                    ],
                ),
                mommy.make(
                    'api_textual.PollAnswer',
                    text='bar',
                    votes=[
                        mommy.make(
                            'api_textual.PollVote',
                            created_at='2016-01-15T13:15:16Z',
                        ),
                    ],
                ),
            ],
        )

        PollVote.objects.filter(pk=1).update(created_at='2016-01-02T13:15:16Z')
        PollVote.objects.filter(pk=2).update(created_at='2016-01-15T13:15:16Z')

        self.assertEquals(
            poll.get_last_vote_date(),
            datetime(2016, 1, 15, 13, 15, 16, tzinfo=pytz.UTC),
        )

    def get_winning_answer(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
            answers=[
                mommy.make(
                    'api_textual.PollAnswer',
                    text='foo',
                    votes=[
                        mommy.make('api_textual.PollVote'),
                        mommy.make('api_textual.PollVote'),
                        mommy.make('api_textual.PollVote'),
                        mommy.make('api_textual.PollVote'),
                    ],
                ),
                mommy.make(
                    'api_textual.PollAnswer',
                    text='bar',
                    votes=[
                        mommy.make('api_textual.PollVote'),
                        mommy.make('api_textual.PollVote'),
                        mommy.make('api_textual.PollVote'),
                    ],
                ),
            ],
        )

        self.assertEquals(
            poll.get_winning_answer(),
            PollAnswer.objects.get(pk=1),
        )

    def get_winning_answer_with_zero_votes(self):
        poll = mommy.make(
            'api_textual.Poll',
            question='Do you like dogs?',
            answers=[
                mommy.make(
                    'api_textual.PollAnswer',
                    text='foo',
                ),
            ],
        )

        self.assertEquals(poll.get_winning_answer(), None)
