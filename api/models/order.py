"""Order model."""
from datetime import datetime

from django.conf import settings
from django.core import mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .payment import Payment
from .participant import Participant
from ..mail import signup as templates
from ..mail.common import formatMail, formatWorkshop


def generate_symvar():
    """Generate variable symbol for a new order."""
    today = datetime.now().strftime('%y%m%d%H%M')
    total = Order.objects.count()
    return "%s%s" % (today, total)


class Order(Base):
    """Stores orders types."""

    participant = models.ForeignKey(Participant, related_name="orders")
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

    def save(self, *args, **kwargs):
        """Generate variable symbol if not available yet."""
        super().save(*args, **kwargs)

        if not self.symvar:
            self.symvar = generate_symvar()
            self.save()

    def __str__(self):
        """Return name as string representation."""
        return "%s at %s" % (self.participant.name, self.created_at)

    def get_mail_confirm_body(self):
        """Format template body to be emailed."""
        workshop = self.reservation.workshop_price.workshop
        workshopFormatted = formatWorkshop({
            'name': workshop.name,
            'lectorName': workshop.lector_names(),
        })

        return formatMail(
            templates.ORDER_CONFIRMED_BODY,
            {
                'price': self.price,
                'symvar': self.symvar,
                'validUntil': self.reservation.ends_at,
                'workshop': workshopFormatted,
            },
        )

    def mail_confirm(self):
        body = self.get_mail_confirm_body()
        mail.send_mail(
            templates.ORDER_CONFIRMED_SUBJECT,
            body,
            settings.EMAIL_SENDER,
            [self.participant.email]
        )

    def confirm(self):
        if not self.confirmed:
            self.confirmed = True
            self.reservation.extend_reservation()
            self.reservation.save()
            self.save()

            payment, _ = Payment.objects.get_or_create(
                symvar=self.symvar,
                defaults={
                    'order': self,
                },
            )
            self.mail_confirm()
