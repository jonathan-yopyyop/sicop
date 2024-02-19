from django.urls import path

from sicop.purchase_order.views import GetPosByCriteria  # noqa,

urlpatterns = [
    path(
        "criteria/search/",
        GetPosByCriteria.as_view(),
        name="purchase_order_list_search_criteria",
    ),
]
