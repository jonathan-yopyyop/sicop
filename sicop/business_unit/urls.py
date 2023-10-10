from django.urls import path

from sicop.business_unit.views import (
    BusinessUnitCreateView,
    BusinessUnitDetailView,
    BusinessUnitListView,
    BusinessUnitUpdateView,
)

urlpatterns = [
    path(
        "list/",
        BusinessUnitListView.as_view(),
        name="business_unit_list",
    ),
    path(
        "detail/<int:pk>/",
        BusinessUnitDetailView.as_view(),
        name="business_unit_detail",
    ),
    path(
        "update/<int:pk>/",
        BusinessUnitUpdateView.as_view(),
        name="business_unit_update",
    ),
    path(
        "create/",
        BusinessUnitCreateView.as_view(),
        name="business_unit_create",
    ),
]
