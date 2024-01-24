from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from sicop.budget.models import (
    Budget,
    BudgetAddition,
    BudgetAdditionApproval,
    BudgetAdditionItem,
    BudgetAddtionTransaction,
    BudgetDecreaseTransaction,
    BudgetDescription,
    BudgetRedistribution,
    BudgetRedistributionItem,
    BudgetRedistributionItemApproval,
    Commitment,
    CommitmentContract,
    CommitmentNotRelated,
    CommitmentPO,
    CommitmentRealeaseItems,
    CommitmentRelease,
    ProvisionCart,
    ProvisionCartApproval,
    ProvisionCartBudget,
)


class BudgetDescriptionResource(resources.ModelResource):
    class Meta:
        model = BudgetDescription


@admin.register(BudgetDescription)
class BudgetDescriptionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetDescriptionResource]
    list_display = (
        "id",
        "expense_concept",
        "description",
    )
    search_fields = (
        "expense_concept",
        "description",
    )


class BudgetResource(resources.ModelResource):
    class Meta:
        model = Budget


@admin.register(Budget)
class BudgetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetResource]
    list_display = (
        "id",
        "budget_description",
        "available_budget",
        "unit_value",
        "quantity",
        "initial_value",
        "budget_addition",
        "budget_decrease",
        "current_budget",
        "created_at",
        "updated_at",
        "status",
    )
    search_fields = (
        "project__name",
        "budget_description__code",
        "start_date",
        "budget_description__code",
    )
    list_filter = (
        "project",
        "budget_description",
        "status",
    )
    readonly_fields = (
        "available_budget",
        "initial_value",
        "budget_addition",
        "budget_decrease",
        "budget_decrease_control",
        "created_at",
        "updated_at",
    )


class ProvisionCartResource(resources.ModelResource):
    class Meta:
        model = ProvisionCart


@admin.register(ProvisionCart)
class ProvisionCartAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProvisionCartResource]
    list_display = (
        "id",
        "project",
        "user",
        "total_provisioned_amount",
        "approved",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "project__name",
        "user__username",
    )
    list_filter = (
        "project",
        "user",
        "status",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


class ProvisionCartBudgetResource(resources.ModelResource):
    class Meta:
        model = ProvisionCartBudget


@admin.register(ProvisionCartBudget)
class ProvisionCartBudgetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProvisionCartBudgetResource]
    list_display = (
        "id",
        "provision_cart",
        "budget",
        "created_at",
        "updated_at",
        "status",
    )
    search_fields = (
        "provision_cart__id",
        "budget__id",
    )
    list_filter = (
        "provision_cart",
        "budget",
        "status",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


class BudgetDecreaseTransactionResource(resources.ModelResource):
    class Meta:
        model = BudgetDecreaseTransaction


@admin.register(BudgetDecreaseTransaction)
class BudgetDecreaseTransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetDecreaseTransactionResource]
    list_display = (
        "id",
        "budget",
        "project",
        "old_amount",
        "new_amount",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "budget__id",
        "project__name",
    )
    list_filter = (
        "budget",
        "project",
    )
    readonly_fields = (
        "id",
        "budget",
        "project",
        "old_amount",
        "new_amount",
        "created_at",
        "updated_at",
    )

    # remove delete, add, change
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProvisionCartApprovalResource(resources.ModelResource):
    class Meta:
        model = ProvisionCartApproval


@admin.register(ProvisionCartApproval)
class ProvisionCartApprovalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProvisionCartApprovalResource]
    list_display = [
        "provision_cart",
        "id",
        "must_be_approved_by",
        "approved",
    ]
    readonly_fields = [
        "id",
        "provision_cart",
        "must_be_approved_by",
        "created_at",
        "updated_at",
    ]


class BudgetRedistributionResource(resources.ModelResource):
    class Meta:
        model = BudgetRedistribution


@admin.register(BudgetRedistribution)
class BudgetRedistributionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetRedistributionResource]
    list_display = [
        "id",
        "budget",
        "original_amount",
        "redistributed_amount",
        "new_amount",
        "requires_approval",
        "approved",
        "must_be_approved_by",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "requires_approval",
        "approved",
        "must_be_approved_by",
        "created_at",
        "updated_at",
    ]


class BudgetRedistributionItemResource(resources.ModelResource):
    class Meta:
        model = BudgetRedistributionItem


@admin.register(BudgetRedistributionItem)
class BudgetRedistributionItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetRedistributionItemResource]
    list_display = [
        "id",
        "budget",
        "original_amount",
        "redistributed_amount",
        "new_amount",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "budget_redistribution",
        "budget",
        "original_amount",
        "created_at",
        "updated_at",
    ]


class BudgetRedistributionItemApprovalResource(resources.ModelResource):
    class Meta:
        model = BudgetRedistributionItemApproval


@admin.register(BudgetRedistributionItemApproval)
class BudgetRedistributionItemApprovalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetRedistributionItemApprovalResource]
    list_display = [
        "id",
        "budget_redistribution_item",
        "approved",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "budget_redistribution_item",
        "created_at",
        "updated_at",
    ]


class BudgetAdditionResource(resources.ModelResource):
    class Meta:
        model = BudgetAddition


@admin.register(BudgetAddition)
class BudgetAdditionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetAdditionResource]
    list_display = [
        "id",
        "requires_approval",
        "approved",
        "must_be_approved_by",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "approved",
        "must_be_approved_by",
        "created_at",
        "updated_at",
    ]


class BudgetAdditionItemResource(resources.ModelResource):
    class Meta:
        model = BudgetAdditionItem


@admin.register(BudgetAdditionItem)
class BudgetAdditionItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetAdditionItemResource]
    list_display = [
        "id",
        "budget",
        "original_amount",
        "added_amount",
        "new_amount",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]


class BudgetAdditionApprovalResource(resources.ModelResource):
    class Meta:
        model = BudgetAdditionApproval


@admin.register(BudgetAdditionApproval)
class BudgetAdditionApprovalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetAdditionApprovalResource]
    list_display = [
        "id",
        "budget_addition",
        "must_be_approved_by",
        "approved",
        "rejected",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "budget_addition",
        "created_at",
        "updated_at",
    ]


class BudgetAddtionTransactionResource(resources.ModelResource):
    class Meta:
        model = BudgetAddtionTransaction


@admin.register(BudgetAddtionTransaction)
class BudgetAddtionTransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [BudgetAddtionTransactionResource]
    list_display = [
        "id",
        "budget",
        "original_amount",
        "added_amount",
        "new_amount",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "budget",
        "created_at",
        "updated_at",
    ]


class CommitmentResource(resources.ModelResource):
    class Meta:
        model = Commitment


@admin.register(Commitment)
class CommitmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CommitmentResource]
    list_display = [
        "id",
        "provision_cart",
        "contract_or_po",
        "third",
        "has_tax",
        "provision_budget_amount",
        "required_amount",
        "diference_between_required_and_provisioned",
        "finished",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "status",
        "tax_amount",
        "user",
        "provision_cart",
        "contract_or_po",
        "third",
        "has_tax",
        "provision_budget_amount",
        "required_amount",
        "diference_between_required_and_provisioned",
        "created_at",
        "updated_at",
    ]


class CommitmentPOResource(resources.ModelResource):
    class Meta:
        model = CommitmentPO


@admin.register(CommitmentPO)
class CommitmentPOAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CommitmentPOResource]
    list_display = [
        "id",
        "commitment",
        "po",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "commitment",
        "po",
        "created_at",
        "updated_at",
    ]


class CommitmentContractResource(resources.ModelResource):
    class Meta:
        model = CommitmentContract


@admin.register(CommitmentContract)
class CommitmentContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CommitmentContractResource]
    list_display = [
        "id",
        "commitment",
        "contract",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "commitment",
        "contract",
        "created_at",
        "updated_at",
    ]


class CommitmentReleaseResource(resources.ModelResource):
    class Meta:
        model = CommitmentRelease


@admin.register(CommitmentRelease)
class CommitmentReleaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CommitmentReleaseResource]
    list_display = [
        "id",
        "commitment",
        "total_to_release",
        "total_released",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "commitment",
        "total_to_release",
        "total_released",
        "created_at",
        "updated_at",
    ]


class CommitmentRealeaseItemsResource(resources.ModelResource):
    class Meta:
        model = CommitmentRealeaseItems


@admin.register(CommitmentRealeaseItems)
class CommitmentRealeaseItemsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CommitmentRealeaseItemsResource]
    list_display = [
        "id",
        "commitment_release",
        "budget",
        "total_to_release",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "commitment_release",
        "budget",
        "total_to_release",
        "created_at",
        "updated_at",
    ]


class CommitmentNotRelatedResource(resources.ModelResource):
    class Meta:
        model = CommitmentNotRelated


@admin.register(CommitmentNotRelated)
class CommitmentNotRelatedAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [CommitmentNotRelatedResource]
    list_display = [
        "id",
        "commitment",
        "type",
        "key",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "commitment",
        "type",
        "key",
        "created_at",
        "updated_at",
    ]
