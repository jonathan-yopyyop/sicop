from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class Certificate(BaseModel):
    """Model definition for Certificate."""

    slug = models.SlugField(
        _("Slug"),
        help_text=_("Slug"),
        unique=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=255,
    )
    version = models.CharField(
        _("Version"),
        help_text=_("Version"),
        max_length=255,
    )
    date = models.DateField(
        _("Date"),
        help_text=_("Date"),
    )

    class Meta:
        """Meta definition for Certificate."""

        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

    def __str__(self):
        """Unicode representation of Certificate."""
        return str(self.id)
