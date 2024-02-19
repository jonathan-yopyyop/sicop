from django.urls import path

from sicop.contract.views import GetContractsByCriteria  # noqa,

urlpatterns = [
    path(
        "criteria/search/",
        GetContractsByCriteria.as_view(),
        name="contract_list_search_criteria",
    ),
]
