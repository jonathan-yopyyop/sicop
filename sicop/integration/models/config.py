from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class ActiveIntegration(BaseModel):
    """Model definition for Active Integration."""

    name = models.CharField(
        _("Name"),
        help_text=_("Name of the integration"),
        max_length=50,
    )
    code = models.SlugField(
        _("Code"),
        help_text=_("Code of the integration"),
        max_length=10,
        unique=True,
    )
    # TODO: Define fields here

    class Meta:
        """Meta definition for Active Integration."""

        verbose_name = "Active Integration"
        verbose_name_plural = "Active Integrations"

    def __str__(self):
        """Unicode representation of Active Integration."""
        return self.name
