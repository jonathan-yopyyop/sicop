from django.urls import path

from sicop.budget.views import (
    AddItemToProvisionInCart,
    AddItemToProvisionInCartHistory,
    AdditionApprovalUpdateView,
    AdditionBudgetApprovalList,
    AdditionCertificateView,
    BudgerReleaseSearchByCommitment,
    BudgerReleaseSearchByConsumption,
    BudgerReleaseSearchByContract,
    BudgerReleaseSearchByLegalization,
    BudgerReleaseSearchByPO,
    BudgetAdditionCreateView,
    BudgetAdditionListView,
    BudgetCapCreateView,
    BudgetCapDetailView,
    BudgetCapListView,
    BudgetCapUpdateView,
    BudgetCreateView,
    BudgetDecreaseTransactionListView,
    BudgetDescriptionCreateView,
    BudgetDescriptionDetailView,
    BudgetDescriptionListView,
    BudgetDescriptionUpdateView,
    BudgetDetailView,
    BudgetListView,
    BudgetProvisionCreate,
    BudgetProvisionDetail,
    BudgetProvisionList,
    BudgetRedistributionCreate,
    BudgetRedistributionDetail,
    BudgetRedistributionListView,
    BudgetRedistributionTransactionListView,
    BudgetRelease,
    BudgetReleaseSearch,
    BudgetUpdateView,
    CommitmentCertificateView,
    CommitmentCreateView,
    CommitmentListView,
    CommitmentReleaseCertificateView,
    CommitmentReleaseListView,
    CommitmentReleaseOrphanUpdateView,
    CommitmentReleaseUpdateView,
    CommitmentTaxUpdateView,
    CreateAdditionItem,
    CreateOrdestroyReleaseTable,
    CreateRedistributionItem,
    EditItemProvisionAmountInCart,
    EditItemProvisionAmountInCartHistory,
    GetBudgetDetailById,
    GetBudgetDetailExceptId,
    GetBudgetIncart,
    GetBudgetIncartHistory,
    GetBudgetsByCostCenterAndProject,
    GetBudgetsByProject,
    GetCostCentersByProject,
    GetProvisionCartsByCriteria,
    ProvisionCartAdditionListView,
    ProvisionCartApprovalList,
    ProvisionCartApprovalUpdateView,
    ProvisionCartSearchView,
    ProvisionCartUpdateView,
    ProvisionCertificateView,
    RedistributionBudgetApprovalList,
    RedistributionBudgetApprovalUpdate,
    RedistributionCertificateView,
    RemoveAdditionItem,
    RemoveItemToProvisionInCart,
    RemoveItemToProvisionInCartHistory,
    RemoveRedistributionItem,
    UpdateAdditionItem,
    UpdateBudgetForRedistribution,
    UpdateCommitmentAmount,
    UpdateCommitmentCap,
    UpdateCommitmentEntity,
    UpdateContractOrPoCap,
    UpdateIdentifier,
    UpdateProjectInCart,
    UpdateRedistributionItem,
    UpdateRedistributionTotals,
    UpdateThirdOrPoCap,
    UpdateTotalsInCart,
    UpdateTotalsInCartHistory,
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
        "budget/project/<int:project_id>/",
        GetBudgetsByProject.as_view(),
        name="get_budgets_by_project",
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
        "budget/provision/criteria/search/",
        GetProvisionCartsByCriteria.as_view(),
        name="get_provision_carts_by_criteria",
    ),
    path(
        "budget/<int:pk>/detail-except/",
        GetBudgetDetailExceptId.as_view(),
        name="get_budget_detail_except_id",
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
    path(
        "budget/decrease_transaction/list/",
        BudgetDecreaseTransactionListView.as_view(),
        name="budget_decrease_control_transaction_list",
    ),
    path(
        "budget/redistribution_transaction/list/",
        BudgetRedistributionTransactionListView.as_view(),
        name="budget_redistribution_transaction_list",
    ),
    path(
        "redistribution/list/",
        BudgetRedistributionListView.as_view(),
        name="budget_redistribution_list",
    ),
    path(
        "redistribution/create/",
        BudgetRedistributionCreate.as_view(),
        name="budget_redistribution_create",
    ),
    path(
        "redistribution/update-budget/",
        UpdateBudgetForRedistribution.as_view(),
        name="update_budget_for_redistribution",
    ),
    path(
        "redistribution/item/create/",
        CreateRedistributionItem.as_view(),
        name="create_redistribution_item",
    ),
    path(
        "redistribution/item/remove/",
        RemoveRedistributionItem.as_view(),
        name="remove_redistribution_item",
    ),
    path(
        "redistribution/item/update/",
        UpdateRedistributionItem.as_view(),
        name="update_redistribution_item",
    ),
    path(
        "redistribution/totals/update/",
        UpdateRedistributionTotals.as_view(),
        name="update_redistribution_totals",
    ),
    path(
        "redistribution/<int:pk>/",
        BudgetRedistributionDetail.as_view(),
        name="budget_redistribution_detail",
    ),
    path(
        "redistribution/approval/list/",
        RedistributionBudgetApprovalList.as_view(),
        name="redistribution_budget_approval_list",
    ),
    path(
        "redistribution/<int:pk>/certificate/",
        RedistributionCertificateView.as_view(),
        name="redistribution_certificate",
    ),
    path(
        "redistribution/approval/update/<int:pk>/",
        RedistributionBudgetApprovalUpdate.as_view(),
        name="redistribution_budget_approval_update",
    ),
    path(
        "addition/list/",
        BudgetAdditionListView.as_view(),
        name="budget_addition_list",
    ),
    path(
        "addition/create/",
        BudgetAdditionCreateView.as_view(),
        name="budget_addition_create",
    ),
    path(
        "addition/item/create/",
        CreateAdditionItem.as_view(),
        name="create_addition_item",
    ),
    path(
        "addition/item/remove/",
        RemoveAdditionItem.as_view(),
        name="remove_addition_item",
    ),
    path(
        "addition/item/update/",
        UpdateAdditionItem.as_view(),
        name="update_addition_item",
    ),
    path(
        "addition/certificate/<int:pk>/",
        AdditionCertificateView.as_view(),
        name="addition_certificate",
    ),
    path(
        "addition/approval/update/<int:pk>/",
        AdditionApprovalUpdateView.as_view(),
        name="addition_approval_update",
    ),
    path(
        "addition/approval/list/",
        AdditionBudgetApprovalList.as_view(),
        name="addition_budget_approval_list",
    ),
    path(
        "commitment/list/",
        CommitmentListView.as_view(),
        name="commitment_list",
    ),
    path(
        "commitment/create/",
        CommitmentCreateView.as_view(),
        name="commitment_create",
    ),
    path(
        "commitment/cap/update/",
        UpdateCommitmentCap.as_view(),
        name="update_commitment_cap",
    ),
    path(
        "commitment/contract-or-po/update/",
        UpdateContractOrPoCap.as_view(),
        name="update_commitment_type",
    ),
    path(
        "commitment/third-or-po/update/",
        UpdateThirdOrPoCap.as_view(),
        name="update_third_cap",
    ),
    path(
        "commitment/contract-or-po/update-entity/",
        UpdateCommitmentEntity.as_view(),
        name="update_cap_entity",
    ),
    path(
        "commitment/release/update/",
        CommitmentReleaseUpdateView.as_view(),
        name="commitment_release_update",
    ),
    path(
        "commitment/tax/update/",
        CommitmentTaxUpdateView.as_view(),
        name="commitment_tax_update",
    ),
    path(
        "commitment/identifier/update/",
        UpdateIdentifier.as_view(),
        name="commitment_identifier_update",
    ),
    path(
        "commitment/amount/update/",
        UpdateCommitmentAmount.as_view(),
        name="commitment_amount_update",
    ),
    path(
        "commitment/release/table/create-or-destroy/",
        CreateOrdestroyReleaseTable.as_view(),
        name="create_or_destroy_release_table",
    ),
    path(
        "commitment/<int:pk>/certificate/",
        CommitmentCertificateView.as_view(),
        name="commitment_certificate",
    ),
    path(
        "commitment/release/search/",
        BudgetReleaseSearch.as_view(),
        name="commitment_release_search",
    ),
    path(
        "commitment/release/search/result/<int:pk>/",
        BudgetRelease.as_view(),
        name="commitment_release",
    ),
    path(
        "commitment/release/search-by-commitment/",
        BudgerReleaseSearchByCommitment.as_view(),
        name="commitment_release_search_by_commitment",
    ),
    path(
        "commitment/release/search-by-contract/",
        BudgerReleaseSearchByContract.as_view(),
        name="commitment_release_search_by_contract",
    ),
    path(
        "commitment/release/search-by-po/",
        BudgerReleaseSearchByPO.as_view(),
        name="commitment_release_search_by_po",
    ),
    path(
        "commitment/release/search-by-legalization/",
        BudgerReleaseSearchByLegalization.as_view(),
        name="commitment_release_search_by_legalization",
    ),
    path(
        "commitment/release/search-by-consumption/",
        BudgerReleaseSearchByConsumption.as_view(),
        name="commitment_release_search_by_consumption",
    ),
    path(
        "commitment/release/orphan/update/",
        CommitmentReleaseOrphanUpdateView.as_view(),
        name="commitment_release_orphan_update",
    ),
    path(
        "commitment/release/certificate/<int:pk>/",
        CommitmentReleaseCertificateView.as_view(),
        name="commitment_release_certificate",
    ),
    path(
        "commitment/release/list/",
        CommitmentReleaseListView.as_view(),
        name="commitment_release_list",
    ),
    path(
        "budget/provision/addition/update/<int:pk>/",
        ProvisionCartUpdateView.as_view(),
        name="budget_arrange_update",
    ),
    path(
        "budget/provision/addition/list/",
        ProvisionCartAdditionListView.as_view(),
        name="budget_arrange_addition_list",
    ),
    path(
        "budget/provision/addition/search/",
        ProvisionCartSearchView.as_view(),
        name="budget_arrange_addition_search",
    ),
    path(
        "budget/provision/cart/history/<int:cart_id>/remove-item/<int:budget_id>",
        RemoveItemToProvisionInCartHistory.as_view(),
        name="remove_item_to_provision_in_cart_history",
    ),
    path(
        "budget/provision/cart/history/<int:cart_id>/",
        UpdateTotalsInCartHistory.as_view(),
        name="update_totals_in_cart_history",
    ),
    path(
        "budget/provision/cart/history/<int:cart_id>/edit-item",
        EditItemProvisionAmountInCartHistory.as_view(),
        name="edit_item_provision_amount_in_cart_history",
    ),
    path(
        "budget/provision/cart/history/<int:cart_id>/add-item/<int:budget_id>",
        AddItemToProvisionInCartHistory.as_view(),
        name="add_item_to_provision_in_cart_history",
    ),
    path(
        "budget/provision/cart/<int:cart_id>/budget/<int:budget_id>/history",
        GetBudgetIncartHistory.as_view(),
        name="get_budget_in_cart_history",
    ),
]
