"""Tests for participant model."""

from django.test import TestCase

from model_mommy import mommy


class PollAnswerTest(TestCase):

    def test_poll_answer_text_representation(self):
        answer = mommy.make(
            'api_textual.PollAnswer',
            text='Yes',
            poll=mommy.make(
                'api_textual.Poll',
                question='Do you like dogs?',
            ),
        )
        self.assertEquals(str(answer), 'Yes (Do you like dogs?)')

    def test_poll_answer_get_vote_count(self):
        answer = mommy.make(
            'api_textual.PollAnswer',
            text='Yes',
            poll=mommy.make(
                'api_textual.Poll',
                question='Do you like dogs?',
            ),
            votes=[
                mommy.make('PollVote'),
                mommy.make('PollVote'),
                mommy.make('PollVote'),
                mommy.make('PollVote'),
            ],
        )
        self.assertEquals(answer.get_vote_count(), 4)
