from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.area.models import Area
from sicop.users.models import User


class ProjectStatus(BaseModel):
    """Model definition for Project Status."""

    code = models.SlugField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Project Status."""

        verbose_name = "Project Status"
        verbose_name_plural = "Project Statuses"

    def __str__(self):
        """Unicode representation of Project Status."""
        return self.name


class ProjectType(BaseModel):
    """Model definition for Project Type."""

    code = models.SlugField(
        _("Code"),
        help_text=_("Code"),
        max_length=150,
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Project Type."""

        verbose_name = "Project Type"
        verbose_name_plural = "Project Types"

    def __str__(self):
        """Unicode representation of Project Type."""
        return self.name


class Project(BaseModel):
    """Model definition for Project."""

    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=150,
    )
    project_id = models.CharField(
        _("Project ID"),
        help_text=_("Project ID"),
        max_length=150,
        blank=True,
        null=True,
    )
    description = models.CharField(
        _("Description"),
        help_text=_("Description"),
        max_length=150,
    )
    start_date = models.DateField(
        _("Start date"),
        help_text=_("Start date"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        _("End date"),
        help_text=_("End date"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    budget = models.DecimalField(
        _("Budget"),
        help_text=_("Budget"),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    project_status = models.ForeignKey(
        ProjectStatus,
        verbose_name=_("Project status"),
        help_text=_("Project status"),
        on_delete=models.CASCADE,
    )
    project_type = models.ForeignKey(
        ProjectType,
        verbose_name=_("Project type"),
        help_text=_("Project type"),
        on_delete=models.CASCADE,
    )
    is_it_taxable = models.BooleanField(
        _("Is it taxable"),
        help_text=_("Is it taxable"),
        default=False,
    )
    area = models.ForeignKey(
        Area,
        verbose_name=_("Area"),
        help_text=_("Area"),
        on_delete=models.CASCADE,
    )
    project_manager = models.ForeignKey(
        User,
        verbose_name=_("Project manager"),
        help_text=_("Project manager"),
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Project."""

        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        """Unicode representation of Project."""
        return self.name


class ProjectStatusHistory(BaseModel):
    """Model definition for Project Status History."""

    project = models.ForeignKey(
        Project,
        verbose_name=_("Project"),
        help_text=_("Project"),
        on_delete=models.CASCADE,
    )
    project_status = models.ForeignKey(
        ProjectStatus,
        verbose_name=_("Project status"),
        help_text=_("Project status"),
        on_delete=models.CASCADE,
    )
    comment = models.TextField(
        _("Comment"),
        help_text=_("Comment"),
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Project Status History."""

        verbose_name = "Project Status History"
        verbose_name_plural = "Project Status Histories"

    def __str__(self):
        """Unicode representation of Project Status History."""
        return self.project.name
