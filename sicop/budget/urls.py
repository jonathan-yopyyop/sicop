from django.urls import path

from sicop.budget.views import (
    AddItemToProvisionInCart,
    BudgetCapCreateView,
    BudgetCapDetailView,
    BudgetCapListView,
    BudgetCapUpdateView,
    BudgetCreateView,
    BudgetDescriptionCreateView,
    BudgetDescriptionDetailView,
    BudgetDescriptionListView,
    BudgetDescriptionUpdateView,
    BudgetDetailView,
    BudgetListView,
    BudgetProvisionCreate,
    BudgetProvisionDetail,
    BudgetProvisionList,
    BudgetUpdateView,
    EditItemProvisionAmountInCart,
    GetBudgetDetailById,
    GetBudgetIncart,
    GetBudgetsByCostCenterAndProject,
    GetCostCentersByProject,
    ProvisionCartApprovalList,
    ProvisionCartApprovalUpdateView,
    ProvisionCertificateView,
    RemoveItemToProvisionInCart,
    UpdateProjectInCart,
    UpdateTotalsInCart,
)

urlpatterns = [
    path(
        "description/list",
        BudgetDescriptionListView.as_view(),
        name="budget_description_list",
    ),
    path(
        "description/create/",
        BudgetDescriptionCreateView.as_view(),
        name="budget_description_create",
    ),
    path(
        "description/<int:pk>/",
        BudgetDescriptionDetailView.as_view(),
        name="budget_description_detail",
    ),
    path(
        "description/<int:pk>/update/",
        BudgetDescriptionUpdateView.as_view(),
        name="budget_description_update",
    ),
    path(
        "budget/list/",
        BudgetListView.as_view(),
        name="budget_list",
    ),
    path(
        "budget/<int:pk>/",
        BudgetDetailView.as_view(),
        name="budget_detail",
    ),
    path(
        "budget/create/",
        BudgetCreateView.as_view(),
        name="budget_create",
    ),
    path(
        "budget/<int:pk>/update/",
        BudgetUpdateView.as_view(),
        name="budget_update",
    ),
    path(
        "budget/cap/list/",
        BudgetCapListView.as_view(),
        name="budget_cap_list",
    ),
    path(
        "budget/cap/create/",
        BudgetCapCreateView.as_view(),
        name="budget_cap_create",
    ),
    path(
        "budget/cap/<int:pk>/",
        BudgetCapDetailView.as_view(),
        name="budget_cap_detail",
    ),
    path(
        "budget/cap/<int:pk>/update/",
        BudgetCapUpdateView.as_view(),
        name="budget_cap_update",
    ),
    path(
        "budget/cost_center/<int:pk>/project/<int:project_id>/",
        GetBudgetsByCostCenterAndProject.as_view(),
        name="get_budgets_by_cost_center",
    ),
    path(
        "budget/provision/create/",
        BudgetProvisionCreate.as_view(),
        name="budget_provision_create",
    ),
    path(
        "budget/<int:pk>/detail/",
        GetBudgetDetailById.as_view(),
        name="get_budget_detail_by_id",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/project/<int:project_id>/",
        UpdateProjectInCart.as_view(),
        name="update_project_in_cart",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/",
        UpdateTotalsInCart.as_view(),
        name="update_totals_in_cart",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/add-item/<int:budget_id>",
        AddItemToProvisionInCart.as_view(),
        name="add_item_to_provision_in_cart",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/remove-item/<int:budget_id>",
        RemoveItemToProvisionInCart.as_view(),
        name="remove_item_to_provision_in_cart",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/edit-item",
        EditItemProvisionAmountInCart.as_view(),
        name="edit_item_provision_amount_in_cart",
    ),
    path(
        "budget/provision/list/",
        BudgetProvisionList.as_view(),
        name="budget_provision_list",
    ),
    path(
        "budget/provision/<int:pk>/",
        BudgetProvisionDetail.as_view(),
        name="budget_provision_detail",
    ),
    path(
        "budget/provision/<int:pk>/certificate/",
        ProvisionCertificateView.as_view(),
        name="provision_certificate",
    ),
    path(
        "budget/cost_center_by_project_id/<int:pk>/",
        GetCostCentersByProject.as_view(),
        name="get_cost_centers_by_project",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/budget/<int:budget_id>/",
        GetBudgetIncart.as_view(),
        name="get_budget_in_cart",
    ),
    path(
        "budget/provision/approval/list/",
        ProvisionCartApprovalList.as_view(),
        name="provision_cart_approval_list",
    ),
    path(
        "budget/provision/approval/update/<int:pk>/",
        ProvisionCartApprovalUpdateView.as_view(),
        name="provision_cart_approval_update",
    ),
]
