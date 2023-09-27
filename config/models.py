from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    status = models.BooleanField(
        _("status"),
        help_text=_("Designates whether this record is active or not."),
        default=True,
    )
    created_at = models.DateTimeField(
        _("created at"),
        help_text=_("Date time on which the object was created."),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        help_text=_("Date time on which the object was last updated."),
        auto_now=True,
    )

    class Meta:
        abstract = True
