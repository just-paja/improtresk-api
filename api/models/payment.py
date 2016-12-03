"""Payment model."""
from django.db import models
from .order import Order
from .base import Base


class Payment(Base):
    """Stores payments."""

    ident = models.CharField(max_length=255, blank=True, unique=True)
    symvar = models.CharField(max_length=255, blank=True)
    symcon = models.CharField(max_length=255, blank=True)
    symspc = models.CharField(max_length=255, blank=True)
    amount = models.CharField(max_length=255)
    sender = models.CharField(max_length=255, blank=True)
    bank = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=255, blank=True)
    received = models.DateTimeField(blank=True, null=True)
    message = models.TextField(max_length=255, blank=True)
    order = models.ForeignKey(Order, blank=True, null=True)
