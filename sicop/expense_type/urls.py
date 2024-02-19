from django.urls import path

from sicop.expense_type.views import (
    ExpenseTypeCreateView,
    ExpenseTypeDetailView,
    ExpenseTypeListView,
    ExpenseTypeUpdatingView,
)

urlpatterns = [
    path(
        "type/list/",
        ExpenseTypeListView.as_view(),
        name="expense_type_list",
    ),
    path(
        "type/create/",
        ExpenseTypeCreateView.as_view(),
        name="expense_type_create",
    ),
    path(
        "type/detail/<int:pk>/",
        ExpenseTypeDetailView.as_view(),
        name="expense_type_detail",
    ),
    path(
        "type/update/<int:pk>/",
        ExpenseTypeUpdatingView.as_view(),
        name="expense_type_update",
    ),
]
