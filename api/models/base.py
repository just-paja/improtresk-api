"""Base model class."""
from django.db import models
from datetime import datetime


class Base(models.Model):
    """Base for all models, adds created_at and updated_at attributes."""

    class Meta:
        """Makes the model abstract."""

        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
