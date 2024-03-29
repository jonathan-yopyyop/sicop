from django.db import models
from config.models import BaseModel


class Report(BaseModel):
    """Model definition for Report."""

    class Meta:
        """Meta definition for Report."""

        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        """Unicode representation of Report."""
        return str(self.id)
