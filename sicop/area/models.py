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

    class Meta:
        """Meta definition for Area Members."""

        verbose_name = _("Area Member")
        verbose_name_plural = _("Area Members")

    def __str__(self):
        """Unicode representation of Area Members."""
        return str(self.user)
