"""Order model."""
from django.db import models
from datetime import datetime
from .base import Base
from .participant import Participant
from .accomodation import Accomodation
from .food import Food
from .workshop import Workshop


def generate_symvar():
    """Generate variable symbol for a new order."""
    today = datetime.now().strftime('%y%m%d%H%M')
    total = Order.objects.count()
    return "%s%s" % (today, total)


class Order(Base):
    """Stores orders types."""

    participant = models.ForeignKey(Participant, related_name="orders")
    symvar = models.CharField(max_length=63, blank=True)
    workshops = models.ManyToManyField(Workshop)
    food = models.ManyToManyField(Food)
    accomodation = models.ManyToManyField(Accomodation)
    price = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)
    overPaid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Generate variable symbol if not available yet."""
        super().save(*args, **kwargs)

        if not self.symvar:
            self.symvar = generate_symvar()
            self.save()
