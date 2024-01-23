from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel
from sicop.budget.models.provision import ProvisionCart
from sicop.contract.models import Contract
from sicop.integration.models import Third
from sicop.purchase_order.models import PurchaseOrder

COMMITMENT_TYPE = (
    ("CT", _("Contract")),
    ("PO", _("Purchase order")),
    ("CO", _("Consumption")),
    ("LG", _("Legalization")),
)


def get_commitment_types():
    return COMMITMENT_TYPE


class Commitment(BaseModel):
    """Model definition for Commitment."""

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        help_text=_("User"),
        related_name="user_commintments",
        on_delete=models.CASCADE,
    )
    provision_cart = models.ForeignKey(
        ProvisionCart,
        verbose_name=_("Provision Cart"),
        help_text=_("Provision Cart"),
        related_name="provision_cart_commitments",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    contract_or_po = models.CharField(
        _("Contract or PO"),
        help_text=_("Contract or PO"),
        max_length=2,
        choices=COMMITMENT_TYPE,
        blank=True,
        null=True,
    )
    third = models.ForeignKey(
        Third,
        verbose_name=_("Third"),
        help_text=_("Third"),
        related_name="third_commitments",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    has_tax = models.BooleanField(
        _("Has tax"),
        help_text=_("Has tax"),
        default=False,
    )
    tax_amount = models.FloatField(
        _("Tax amount"),
        help_text=_("Tax amount"),
        default=0,
        null=True,
        blank=True,
    )
    provision_budget_amount = models.FloatField(
        _("Provision budget amount"),
        help_text=_("Provision budget amount"),
        default=0,
        null=True,
        blank=True,
    )
    required_amount = models.FloatField(
        _("Required amount"),
        help_text=_("Required amount"),
        default=0,
        null=True,
        blank=True,
    )
    diference_between_required_and_provisioned = models.FloatField(
        _("Difference between required and provisioned"),
        help_text=_("Difference between required and provisioned"),
        default=0,
        null=True,
        blank=True,
    )
    finished = models.BooleanField(
        _("Finished"),
        help_text=_("Finished"),
        default=False,
    )

    class Meta:
        """Meta definition for Commitment."""

        verbose_name = _("Commitment")
        verbose_name_plural = _("Commitments")

    def __str__(self):
        """Unicode representation of Commitment."""
        return str(self.id)


class CommitmentPO(BaseModel):
    """Model definition for Commitment PO."""

    commitment = models.ForeignKey(
        Commitment,
        verbose_name=_("Commitment"),
        help_text=_("Commitment"),
        related_name="commitment_po",
        on_delete=models.CASCADE,
    )
    po = models.ForeignKey(
        PurchaseOrder,
        verbose_name=_("Purchase Order"),
        help_text=_("Purchase Order"),
        related_name="purchase_order_commitment_po",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Commitment PO."""

        verbose_name = _("Commitment PO")
        verbose_name_plural = _("Commitment POs")

    def __str__(self):
        """Unicode representation of Commitment PO."""
        return str(self.id)


class CommitmentContract(BaseModel):
    """Model definition for Commitment Contract."""

    commitment = models.ForeignKey(
        Commitment,
        verbose_name=_("Commitment"),
        help_text=_("Commitment"),
        related_name="commitment_contract",
        on_delete=models.CASCADE,
    )
    contract = models.ForeignKey(
        Contract,
        verbose_name=_("Contract"),
        help_text=_("Contract"),
        related_name="contract_commitment_po",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Commitment Contract."""

        verbose_name = _("Commitment Contract")
        verbose_name_plural = _("Commitment Contracts")

    def __str__(self):
        """Unicode representation of Commitment contract."""
        return str(self.id)


class CommitmentNotRelated(BaseModel):
    """Model definition for Commitment Not Related."""

    commitment = models.ForeignKey(
        Commitment,
        verbose_name=_("Commitment"),
        help_text=_("Commitment"),
        related_name="commitment_not_related",
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        _("Type"),
        help_text=_("Type"),
        max_length=2,
        choices=COMMITMENT_TYPE,
        blank=True,
        null=True,
    )
    key = models.CharField(
        _("Key"),
        help_text=_("Key"),
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Commitment Not Related."""

        verbose_name = _("Commitment No related")
        verbose_name_plural = _("Commitment Not related")

    def __str__(self):
        """Unicode representation of Commitment Not Related."""
        return str(self.id)


class CommitmentRelease(BaseModel):
    """Model definition for Commitment Release."""

    commitment = models.ForeignKey(
        Commitment,
        verbose_name=_("Commitment"),
        help_text=_("Commitment"),
        related_name="commitment_release",
        on_delete=models.CASCADE,
    )
    total_to_release = models.FloatField(
        _("Total to release"),
        help_text=_("Total to release"),
        default=0,
        null=True,
        blank=True,
    )
    total_released = models.FloatField(
        _("Total released"),
        help_text=_("Total released"),
        default=0,
        null=True,
        blank=True,
    )

    @property
    def total_pending(self):
        return self.total_to_release - self.total_released

    class Meta:
        """Meta definition for Commitment Release."""

        verbose_name = _("Commitment Release")
        verbose_name_plural = _("Commitment Releases")

    def __str__(self):
        """Unicode representation of Commitment Release."""
        return str(self.id)


class CommitmentRealeaseItems(BaseModel):
    """Model definition for Commitment Realease Items."""

    commitment_release = models.ForeignKey(
        CommitmentRelease,
        verbose_name=_("Commitment Release"),
        help_text=_("Commitment Release"),
        related_name="commitment_release_items",
        on_delete=models.CASCADE,
    )
    budget = models.ForeignKey(
        "budget.Budget",
        verbose_name=_("Budget"),
        help_text=_("Budget"),
        related_name="budget_commitment_release_items",
        on_delete=models.CASCADE,
    )
    budget_amount = models.FloatField(
        _("Budget amount"),
        help_text=_("Budget amount"),
        default=0,
        null=True,
        blank=True,
    )
    total_to_release = models.FloatField(
        _("Total to release"),
        help_text=_("Total to release"),
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Commitment Realease Items."""

        verbose_name = _("Commitment Realease Item")
        verbose_name_plural = _("Commitment Realease Items")

    def __str__(self):
        """Unicode representation of Commitment Realease Items."""
        return str(self.id)
