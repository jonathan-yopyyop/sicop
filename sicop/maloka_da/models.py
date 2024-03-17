from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        help_text=_("Date time on which the object was created"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Date time on which the object was last updated"),
        auto_now=True,
    )
    status = models.BooleanField(
        _("Status"),
        help_text=_("Object status"),
        default=True,
    )

    class Meta:
        abstract = True


class ActiveDirectoryCredential(BaseModel):
    """Model definition for Active Directory Credentials."""

    domain = models.CharField(
        _("Domain"),
        help_text=_("Active Directory domain"),
        max_length=255,
    )
    domain_extension = models.CharField(
        _("Domain Extension"),
        help_text=_("Active Directory domain extension"),
        max_length=255,
    )
    username = models.CharField(
        _("Username"),
        help_text=_("Active Directory username"),
        max_length=255,
    )
    password = models.CharField(
        _("Password"),
        help_text=_("Active Directory password"),
        max_length=255,
    )

    class Meta:
        """Meta definition for Active Directory Credentials."""

        unique_together = ["domain", "domain_extension"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(domain__isnull=False) & models.Q(domain_extension__isnull=False),
                name="%(app_label)s_%(class)s_both_fields_not_null",
            )
        ]

        verbose_name = _("Active Directory Credential")
        verbose_name_plural = _("Active Directory Credentialss")

    def __str__(self):
        """Unicode representation of Active Directory Credentials."""
        return f"{self.domain}.{self.domain_extension}"


class OrganizationalUnit(BaseModel):
    """Model definition for Organizational Unit."""

    credential = models.ForeignKey(
        ActiveDirectoryCredential,
        on_delete=models.CASCADE,
        help_text=_("Active Directory credential"),
    )
    OU = models.CharField(
        _("Organizational Unit"),
        help_text=_("Active Directory Organizational Unit"),
        max_length=255,
    )

    class Meta:
        """Meta definition for Organizational Unit."""

        verbose_name = _("Organizational Unit")
        verbose_name_plural = _("Organizational Units")

    def __str__(self):
        """Unicode representation of Organizational Unit."""
        return f"{self.OU}"


class ActiveDirectoryUser(BaseModel):
    """Model definition for Active Directory User."""

    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        help_text=_("Active Directory Organizational Unit"),
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Active Directory user name"),
        max_length=255,
    )
    user = models.CharField(
        _("User"),
        help_text=_("Active Directory user"),
        max_length=255,
    )

    class Meta:
        """Meta definition for Active Directory User."""

        verbose_name = _("Active Directory User")
        verbose_name_plural = _("Active Directory Users")

    def __str__(self):
        """Unicode representation of Active Directory User."""
        return f"{self.name}"
