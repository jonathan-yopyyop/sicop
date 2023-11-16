from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.users.models import User

# Create a django model that conatins the fields for the accountar company Area model.


class Area(BaseModel):
    """Model definition for Area."""

    name = models.CharField(
        _("Area name"),
        help_text=_("Area name"),
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        _("Area description"),
        help_text=_("Area description"),
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Area."""

        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        """Unicode representation of Area."""
        return self.name


class AreaMember(BaseModel):
    """Model definition for Area Members."""

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        help_text=_("User"),
        on_delete=models.CASCADE,
    )
    area = models.ForeignKey(
        Area,
        verbose_name=_("Area"),
        help_text=_("Area"),
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        "AreaRole",
        verbose_name=_("Area Role"),
        help_text=_("Area Role"),
        on_delete=models.DO_NOTHING,
    )

    @property
    def user_full_name(self):
        return self.user.name

    class Meta:
        """Meta definition for Area Members."""

        verbose_name = _("Area Member")
        verbose_name_plural = _("Area Members")

    def __str__(self):
        """Unicode representation of Area Members."""
        return str(self.user)


class AreaRole(BaseModel):
    """Model definition for Area Role."""

    code = models.CharField(
        _("Area Role code"),
        help_text=_("Area Role code"),
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        _("Area Role name"),
        help_text=_("Area Role name"),
        max_length=150,
        unique=True,
    )

    class Meta:
        """Meta definition for Area Role."""

        verbose_name = "Area Role"
        verbose_name_plural = "Area Roles"

    def __str__(self):
        """Unicode representation of Area Role."""
        return self.name
