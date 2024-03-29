from django.contrib.auth.models import AbstractUser, Permission
from django.db.models import BooleanField, CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from sicop.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for SICOP.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(
        _("Name of User"),
        blank=True,
        max_length=255,
    )
    job_title = CharField(
        _("Job Title"),
        blank=True,
        max_length=255,
        default="",
    )
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(
        _("email address"),
        unique=True,
    )
    username = None  # type: ignore
    status = BooleanField(
        _("Status"),
        default=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


def permission_string_method(self):
    names = self.name.split()
    operation_translated = " ".join(
        [
            _(w)
            .replace("Can", str(_("Can")))
            .replace("add", str(_("add")))
            .replace("change", str(_("change")))
            .replace("delete", str(_("delete")))
            .replace("view", str(_("view")))
            .replace("log", "")
            .replace("content", "")
            .strip()
            for w in names[:-1]  # Exclude the last word (model name)
        ]
    )
    return f"{operation_translated} | {self.content_type.name}"


Permission.__str__ = permission_string_method
