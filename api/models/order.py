"""Order model."""

from django.conf import settings
from django.core import mail
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from .participant import Participant
from .payment import STATUS_PAID
from .reservation import Reservation
from .workshop import Workshop
from .participantWorkshop import ParticipantWorkshop
from .year import Year


def generate_symvar():
    """Generate variable symbol for a new order."""
    today = now().strftime('%Y')
    top = Order.objects.filter(symvar__startswith=today).order_by('id').last()

    if top:
        total = int(top.symvar[4:].split(today)[-1]) + 1
    else:
        total = 1

    return "%s%s" % (today, total)


class Order(Base):
    """Stores orders types."""

    year = models.ForeignKey(
        'Year',
        null=True,
        related_name='orders',
        on_delete=models.PROTECT,
    )
    participant = models.ForeignKey(
        Participant,
        related_name="orders",
        on_delete=models.CASCADE,
    )
    symvar = models.CharField(
        verbose_name=_("Variable symbol"),
        max_length=63,
        blank=True,
        unique=True,
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Definitive price"),
        null=True,
    )
    paid = models.BooleanField(
        default=False,
        verbose_name=_("Is paid?"),
    )
    confirmed = models.BooleanField(
        default=False,
        verbose_name=_("Is confirmed?"),
    )
    over_paid = models.BooleanField(default=False)
    canceled = models.BooleanField(
        verbose_name=_("Is canceled?"),
        default=False,
    )
    accomodation_info = models.BooleanField(
        verbose_name=_("Send extra info about accomodation"),
        default=False,
    )

    class Meta:
        ordering = ('-created_at', )

    def __init__(self, *args, **kwargs):
        """Store initial paid status."""
        super().__init__(*args, **kwargs)
        self.initialPaid = self.paid
        self.initialPrice = self.price
        self.initialConfirmed = self.confirmed

    def __str__(self):
        """Return name as string representation."""
        return "%s at %s" % (self.participant.name, self.created_at)

    def save(self, *args, **kwargs):
        """Generate variable symbol if not available yet."""

        if not self.symvar:
            self.symvar = generate_symvar()

        super().save(*args, **kwargs)

        if not self.initialConfirmed and self.confirmed:
            self.mail_confirm()

    def get_mail_body(self, template):
        """Format template body to be emailed."""
        return render_to_string(
            template,
            {
                'account_info': {
                    'price': self.amount_left(),
                    'symvar': self.symvar,
                },
                'amount_paid': self.total_amount_received(),
                'amount_left': self.amount_left(),
                'price': self.price,
                'payments': self.payments.all(),
                'symvar': self.symvar,
                'validUntil': self.reservation.ends_at,
                'workshop': self.reservation.workshop(),
            },
        )

    def has_reservation(self):
        try:
            return self.reservation is not None
        except Reservation.DoesNotExist:
            return False

    def mail_confirm(self):
        if self.has_reservation():
            mail.send_mail(
                'Tvoje přihláška',
                self.get_mail_body('mail/order_confirmed.txt'),
                settings.EMAIL_SENDER,
                [self.participant.email],
            )

    def mail_paid(self):
        mail.send_mail(
            'Přihláška zaplacena',
            self.get_mail_body('mail/order_paid.txt'),
            settings.EMAIL_SENDER,
            [self.participant.email],
        )

    def mail_update(self):
        mail.send_mail(
            'Aktualizace stavu přihlášky',
            self.get_mail_body('mail/order_update.txt'),
            settings.EMAIL_SENDER,
            [self.participant.email],
        )

    def confirm(self):
        if not self.confirmed:
            self.confirmed = True
            self.reservation.extend_reservation()
            self.reservation.save()
            self.save()

    def amount_left(self):
        return max(0, self.price - self.total_amount_received())

    def total_amount_received(self):
        paid = self.payments\
            .filter(status=STATUS_PAID)\
            .aggregate(total=models.Sum('amount'))
        return paid['total'] if paid['total'] else 0

    def update_paid_status(self):
        paid_price = self.total_amount_received()
        self.paid = paid_price >= self.price
        self.over_paid = paid_price > self.price
        self.save()
        if self.paid:
            if not self.initialPaid:
                self.mail_paid()

            if not self.participant.get_assignment(self.year):
                self.try_to_assign()
        else:
            self.mail_update()

    def try_to_assign(self):
        if not self.reservation.workshop_price:
            return

        ambiguous = ambiguous_orders()
        ambiguous_count = ambiguous.count()

        if ambiguous_count == 0:
            assignment = ParticipantWorkshop(
                participant=self.participant,
                year=self.year,
                workshop=self.reservation.workshop(),
            )
            assignment.save()
        else:
            formatConfig = {
                'order': self.id,
                'participant': self.participant.name,
                'workshop': self.reservation.workshop().name,
            }
            mail.send_mail(
                '[O{order}]: Nepovedlo se zařadit na workshop'.format(
                    **formatConfig,
                ),
                render_to_string('mail/assignment_failed.txt', formatConfig),
                settings.EMAIL_SENDER,
                [settings.EMAIL_TECH],
            )


def unassigned_orders():
    year = Year.objects.get_current()
    if not year:
        return Order.objects.none()
    return Order.objects.filter(
        year=year,
        paid=True,
        participant__workshops__workshop__exact=models.F('reservation__workshop_price__workshop'),
    )


def workshops_at_capacity():
    year = Year.objects.get_current()
    if not year:
        return Workshop.objects.none()
    return Workshop.objects\
        .filter(year=year)\
        .annotate(assignees=models.Count('participant'))\
        .filter(assignees__gte=models.F('capacity'))


def ambiguous_orders():
    """
        Get orders that cannot be really assigned because their destination
        workshop is full.
    """
    workshops_full = workshops_at_capacity()
    return unassigned_orders().filter(
        reservation__workshop_price__workshop__in=workshops_full,
    )
