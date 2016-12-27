"""Base model class."""
from django.db import models
from datetime import datetime


class Base(models.Model):
    """Base for all models, adds createdAt and updatedAt attributes."""

    class Meta:
        """Makes the model abstract."""

        abstract = True

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
