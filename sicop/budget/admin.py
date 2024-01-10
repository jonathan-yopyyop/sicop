from django.contrib import admin

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
    ProvisionCart,
    ProvisionCartApproval,
    ProvisionCartBudget,
)


@admin.register(BudgetDescription)
class BudgetDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "expense_concept",
        "description",
    )
    search_fields = (
        "expense_concept",
        "description",
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
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


@admin.register(ProvisionCart)
class ProvisionCartAdmin(admin.ModelAdmin):
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


@admin.register(ProvisionCartBudget)
class ProvisionCartBudgetAdmin(admin.ModelAdmin):
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


@admin.register(BudgetDecreaseTransaction)
class BudgetDecreaseTransactionAdmin(admin.ModelAdmin):
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


@admin.register(ProvisionCartApproval)
class ProvisionCartApprovalAdmin(admin.ModelAdmin):
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


@admin.register(BudgetRedistribution)
class BudgetRedistributionAdmin(admin.ModelAdmin):
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


@admin.register(BudgetRedistributionItem)
class BudgetRedistributionItemAdmin(admin.ModelAdmin):
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


@admin.register(BudgetRedistributionItemApproval)
class BudgetRedistributionItemApprovalAdmin(admin.ModelAdmin):
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


@admin.register(BudgetAddition)
class BudgetAdditionAdmin(admin.ModelAdmin):
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


@admin.register(BudgetAdditionItem)
class BudgetAdditionItemAdmin(admin.ModelAdmin):
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


@admin.register(BudgetAdditionApproval)
class BudgetAdditionApprovalAdmin(admin.ModelAdmin):
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


@admin.register(BudgetAddtionTransaction)
class BudgetAddtionTransactionAdmin(admin.ModelAdmin):
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
