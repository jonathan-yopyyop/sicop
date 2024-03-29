from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from config.models import BaseModel
from sicop.area.models import Area
from sicop.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

        verbose_name = _("Project Status")
        verbose_name_plural = _("Project Statuses")

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
    cap = models.FloatField(
        _("Cap"),
        help_text=_("Cap"),
        default=0.0,
    )
    redistribution_cap = models.FloatField(
        _("Redistribution Cap"),
        help_text=_("Redistribution Cap"),
        default=0.0,
    )

    class Meta:
        """Meta definition for Project Type."""

        verbose_name = _("Project Type")
        verbose_name_plural = _("Project Types")

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
    budget = models.FloatField(
        _("Budget"),
        help_text=_("Budget"),
        null=True,
        blank=True,
        default=0.0,
    )
    project_status = models.ForeignKey(
        ProjectStatus,
        verbose_name=_("Project status"),
        help_text=_("Project status"),
        on_delete=models.DO_NOTHING,
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
    is_closed = models.BooleanField(
        _("Is closed"),
        help_text=_("Is closed"),
        default=False,
    )
    closed_datetime = models.DateTimeField(
        _("Closed datetime"),
        help_text=_("Closed datetime"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Project."""

        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

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

        verbose_name = _("Project Status History")
        verbose_name_plural = _("Project Status Histories")

    def __str__(self):
        """Unicode representation of Project Status History."""
        return self.project.name


@receiver(post_save, sender=Project)
def project_post_save(sender, instance, created, **kwargs):
    if created:
        new_object = instance
        try:
            project_status = ProjectStatus.objects.get(id=1)
            ProjectStatusHistory.objects.create(
                project=new_object,
                project_status=project_status,
                comment=_("El proyecto fue creado el:") + " " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        except Exception as e:
            print(f"+++++++++++{e}")
