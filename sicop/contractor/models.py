from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class Contractor(BaseModel):
    """Model definition for Contractor."""

    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )
    commertial_name = models.CharField(
        _("Commertial name"),
        help_text=_("Commertial name"),
        max_length=150,
    )
    phone = models.CharField(
        _("Phone"),
        help_text=_("Phone"),
        max_length=150,
        null=True,
        blank=True,
    )
    address = models.CharField(
        _("Address"),
        help_text=_("Address"),
        max_length=250,
        null=True,
        blank=True,
    )
    dni = models.CharField(
        _("DNI"),
        help_text=_("DNI"),
        max_length=150,
        unique=True,
    )

    class Meta:
        """Meta definition for Contractor."""

        verbose_name = _("Contractor")
        verbose_name_plural = _("Contractors")

    def __str__(self):
        """Unicode representation of Contractor."""
        return f"{self.name}"


class ContractorFile(BaseModel):
    """Model definition for Contractor File."""

    contractor = models.ForeignKey(
        Contractor,
        verbose_name=_("Contractor"),
        help_text=_("Contractor"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        _("File"),
        help_text=_("File"),
        upload_to="contractor_files",
    )

    class Meta:
        """Meta definition for Contractor File."""

        verbose_name = _("Contractor File")
        verbose_name_plural = _("Contractor Files")

    def __str__(self):
        """Unicode representation of Contractor File."""
        return str(self.contractor)
