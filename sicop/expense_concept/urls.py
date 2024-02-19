from django.urls import path

from sicop.expense_concept.views import (
    ExpenseConceptCreateView,
    ExpenseConceptDetailView,
    ExpenseConceptListView,
    ExpenseConceptUpdateView,
)

urlpatterns = [
    path(
        "concept/list/",
        ExpenseConceptListView.as_view(),
        name="expense_concept_list",
    ),
    path(
        "concept/detail/<int:pk>/",
        ExpenseConceptDetailView.as_view(),
        name="expense_concept_detail",
    ),
    path(
        "concept/create/",
        ExpenseConceptCreateView.as_view(),
        name="expense_concept_create",
    ),
    path(
        "concept/update/<int:pk>/",
        ExpenseConceptUpdateView.as_view(),
        name="expense_concept_update",
    ),
]
