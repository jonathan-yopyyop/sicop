from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel

CONTRACTOR_TYPES = (
    ("1", _("Natural Person")),
    ("2", _("Legal Person")),
)


class Contractor(BaseModel):
    """Model definition for Contractor."""

    first_name = models.CharField(
        _("First name"),
        help_text=_("First name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Last name"),
        help_text=_("Last name"),
        max_length=150,
    )
    email = models.EmailField(
        _("Email"),
        help_text=_("Email"),
        max_length=254,
    )
    phone = models.CharField(
        _("Phone"),
        help_text=_("Phone"),
        max_length=150,
    )
    address = models.CharField(
        _("Address"),
        help_text=_("Address"),
        max_length=150,
        null=True,
        blank=True,
    )
    dni = models.CharField(
        _("DNI"),
        help_text=_("DNI"),
        max_length=150,
        unique=True,
    )
    contractor_type = models.CharField(
        _("Contractor type"),
        help_text=_("Contractor type"),
        max_length=150,
        choices=CONTRACTOR_TYPES,
    )

    class Meta:
        """Meta definition for Contractor."""

        verbose_name = _("Contractor")
        verbose_name_plural = _("Contractors")

    def __str__(self):
        """Unicode representation of Contractor."""
        return f"{self.first_name} {self.last_name}"


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
