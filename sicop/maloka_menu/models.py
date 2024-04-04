from django.db import models
from config.models import BaseModel
from django.utils.translation import gettext_lazy as _
from sicop.area.models import AreaRole
from django.contrib.auth.models import Group, Permission


class MenuGroup(BaseModel):
    """Model definition for Menu Group."""

    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )
    order = models.IntegerField(
        _("Order"),
        help_text=_("Order"),
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Menu Group."""

        verbose_name = _("Menu Group")
        verbose_name_plural = _("Menu Groups")

    def __str__(self):
        """Unicode representation of Menu Group."""
        return self.name


class Menu(BaseModel):
    """Model definition for Menu."""

    menu = models.CharField(
        _("Menu"),
        help_text=_("Menu"),
        max_length=150,
    )
    group = models.ForeignKey(
        MenuGroup,
        verbose_name=_("Menu Group"),
        help_text=_("Menu Group"),
        related_name="menu_group",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    icon = models.CharField(
        _("Icon"),
        help_text=_("Icon"),
        max_length=150,
    )
    slug = models.SlugField(
        _("Slug"),
        help_text=_("Slug"),
        max_length=150,
        unique=True,
    )

    class Meta:
        """Meta definition for Menu."""

        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        """Unicode representation of Menu."""
        return self.menu


class MenuOption(BaseModel):
    """Model definition for Menu Option."""

    menu = models.ForeignKey(
        Menu,
        verbose_name=_("Menu"),
        help_text=_("Menu"),
        related_name="menu_options",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )
    url_name = models.CharField(
        _("URL name"),
        help_text=_("URL name"),
        max_length=250,
        default="#",
    )
    url_complement = models.CharField(
        _("URL complement"),
        help_text=_("URL complement"),
        max_length=250,
        default="/",
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("Permissions"),
        help_text=_("Permissions"),
        related_name="menu_options",
    )
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("Security groups"),
        help_text=_("Security groups"),
        related_name="menu_options",
    )
    roles = models.ManyToManyField(
        AreaRole,
        verbose_name=_("Security roles"),
        help_text=_("Security roles"),
        related_name="menu_options",
    )
    special_roles = models.ManyToManyField(
        AreaRole,
        verbose_name=_("Special roles"),
        help_text=_("Special roles"),
        related_name="menu_special_options",
    )

    class Meta:
        """Meta definition for Menu Option."""

        verbose_name = _("Menu Option")
        verbose_name_plural = _("Menu Options")

    def __str__(self):
        """Unicode representation of Menu Option."""
        return self.name
