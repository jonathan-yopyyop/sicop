from django.urls import path

from sicop.area.views import (
    AreaCreateView,
    AreaDetailView,
    AreaListView,
    AreaMemberCreateView,
    AreaMemberDetailView,
    AreaMemberListView,
    AreaMemberUpdateView,
    AreaUpdateView,
)

urlpatterns = [
    path(
        "areas/list",
        AreaListView.as_view(),
        name="area_area_list",
    ),
    path(
        "areas/detail/<int:pk>",
        AreaDetailView.as_view(),
        name="area_area_detail",
    ),
    path(
        "areas/update/<int:pk>",
        AreaUpdateView.as_view(),
        name="area_area_update",
    ),
    path(
        "areas/create",
        AreaCreateView.as_view(),
        name="area_area_create",
    ),
    path(
        "member/list",
        AreaMemberListView.as_view(),
        name="area_member_list",
    ),
    path(
        "member/detail/<int:pk>",
        AreaMemberDetailView.as_view(),
        name="area_member_detail",
    ),
    path(
        "member/update/<int:pk>",
        AreaMemberUpdateView.as_view(),
        name="area_member_update",
    ),
    path(
        "member/create",
        AreaMemberCreateView.as_view(),
        name="area_member_create",
    ),
]
