"""Tests for participant model."""

from django.core import mail
from django.test import TestCase
from model_mommy import mommy

from api.models import ParticipantWorkshop


class ParticipantWorkshopAssignmentTest(TestCase):
    def setUp(self):
        mail.outbox = []
        mommy.make(
            'api.ParticipantWorkshop',
            participant__name='Henry Black',
            participant__email='participant@example.com',
            workshop__name='Tiny Afterlunch Workshop',
        )

    def test_mail_sent_to_participant_email(self):
        self.assertEquals(mail.outbox.pop().to, ['participant@example.com'])

    def test_mail_contains_workshop_name(self):
        self.assertIn('Tiny Afterlunch Workshop', mail.outbox.pop().body)


class ParticipantWorkshopReassignmentTest(TestCase):
    def setUp(self):
        gen_assignment = mommy.make(
            'api.ParticipantWorkshop',
            participant__name='Henry Black',
            participant__email='participant@example.com',
            workshop__name='Tiny Afterlunch Workshop',
        )
        second_workshop = mommy.make(
            'api.Workshop',
            name='Large Breakfast Workshop',
        )
        mail.outbox = []
        assignment = ParticipantWorkshop.objects.get(pk=gen_assignment.id)
        assignment.workshop = second_workshop
        assignment.save()

    def test_mail_sent_to_participant_email(self):
        self.assertEquals(mail.outbox.pop().to, ['participant@example.com'])

    def test_mail_contains_previous_workshop_name(self):
        self.assertIn('Tiny Afterlunch Workshop', mail.outbox.pop().body)

    def test_mail_contains_current_workshop_name(self):
        self.assertIn('Large Breakfast Workshop', mail.outbox.pop().body)


class ParticipantWorkshopRemoveTest(TestCase):
    def setUp(self):
        assignment = mommy.make(
            'api.ParticipantWorkshop',
            participant__name='Henry Black',
            participant__email='participant@example.com',
            workshop__name='Tiny Afterlunch Workshop',
        )
        mail.outbox = []
        assignment.delete()

    def test_mail_sent_to_participant_email(self):
        self.assertEquals(mail.outbox.pop().to, ['participant@example.com'])

    def test_mail_contains_previous_workshop_name(self):
        self.assertIn('Tiny Afterlunch Workshop', mail.outbox.pop().body)
