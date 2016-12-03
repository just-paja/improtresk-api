"""Base model class."""
from django.db import models
from datetime import datetime


class Base(models.Model):
    """Base for all models, adds createdAt and updatedAt attributes."""

    class Meta:
        """Defines photo as abstract class."""

        abstract = True

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Update createdAt and updatedAt on save."""
        if not self.pk:
            self.createdAt = datetime.now()

        self.updatedAt = datetime.now()
        super(Base, self).save(*args, **kwargs)
