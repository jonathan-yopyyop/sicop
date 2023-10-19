from django.urls import path

from sicop.budget.views import (
    BudgetDescriptionCreateView,
    BudgetDescriptionDetailView,
    BudgetDescriptionListView,
    BudgetDescriptionUpdateView,
)

urlpatterns = [
    path(
        "description/",
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
]
