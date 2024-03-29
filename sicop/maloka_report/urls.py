from django.urls import path
from sicop.maloka_report.views import (
    ReportHomeView,
    ReportByAreasView,
    ReportByProjectView,
    ReportProjectDetailView,
    ReportSelectBussinesUnitView,
    ReportBussinesUnitView,
)

urlpatterns = [
    path(
        "principal/home/",
        ReportHomeView.as_view(),
        name="report_home",
    ),
    path(
        "principal/areas/",
        ReportByAreasView.as_view(),
        name="report_by_areas",
    ),
    path(
        "principal/projects/<int:area>/area/",
        ReportByProjectView.as_view(),
        name="report_by_project",
    ),
    path(
        "principal/projects/<int:project>/project/",
        ReportProjectDetailView.as_view(),
        name="report_project_detail",
    ),
    path(
        "principal/select_bussines_unit/",
        ReportSelectBussinesUnitView.as_view(),
        name="select_bussines_unit",
    ),
    path(
        "principal/bussines_unit/<int:business_unit>/",
        ReportBussinesUnitView.as_view(),
        name="report_bussines_unit",
    ),
]
