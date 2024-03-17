from django.urls import path

from sicop.integration.views import GetThirdByCriteria  # noqa,

urlpatterns = [
    path(
        "third/criteria/search/",
        GetThirdByCriteria.as_view(),
        name="third_list_search_criteria",
    ),
]
