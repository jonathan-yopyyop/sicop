from django.urls import path

from sicop.budget.views import (
    BudgetCreateView,
    BudgetDescriptionCreateView,
    BudgetDescriptionDetailView,
    BudgetDescriptionListView,
    BudgetDescriptionUpdateView,
    BudgetDetailView,
    BudgetListView,
    BudgetUpdateView,
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
        "budget/budget/list/",
        BudgetListView.as_view(),
        name="budget_list",
    ),
    path(
        "budget/budget/<int:pk>/",
        BudgetDetailView.as_view(),
        name="budget_detail",
    ),
    path(
        "budget/budget/create/",
        BudgetCreateView.as_view(),
        name="budget_create",
    ),
    path(
        "budget/budget/<int:pk>/update/",
        BudgetUpdateView.as_view(),
        name="budget_update",
    ),
]
