from django.urls import path

from sicop.cost_center.views import (
    CostCenterCreateView,
    CostCenterDetailView,
    CostCenterListView,
    CostCenterUpdateView,
)

urlpatterns = [
    path(
        "list/",
        CostCenterListView.as_view(),
        name="cost_center_list",
    ),
    path(
        "detail/<int:pk>/",
        CostCenterDetailView.as_view(),
        name="cost_center_detail",
    ),
    path(
        "uptade/<int:pk>/update/",
        CostCenterUpdateView.as_view(),
        name="cost_center_update",
    ),
    path(
        "create/",
        CostCenterCreateView.as_view(),
        name="cost_center_create",
    ),
]
