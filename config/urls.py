from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from config.views import HomeView
from sicop.sicop_error_handler.views import (
    custom_400,
    custom_401,
    custom_403,
    custom_404,
    custom_500,
    custom_501,
    custom_502,
    custom_503,
)

urlpatterns = i18n_patterns(
    path(
        settings.ADMIN_URL,
        admin.site.urls,
    ),
    path(
        "home/",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "",
        HomeView.as_view(),
        name="index_home",
    ),
    path(
        "user/",
        include("sicop.users.urls"),
    ),
    path(
        "area/",
        include("sicop.area.urls"),
    ),
    path(
        "expense/",
        include("sicop.expense_concept.urls"),
    ),
    path(
        "expense/",
        include("sicop.expense_type.urls"),
    ),
    path(
        "cost_center/",
        include("sicop.cost_center.urls"),
    ),
    path(
        "business_unit/",
        include("sicop.business_unit.urls"),
    ),
    path(
        "budget/",
        include("sicop.budget.urls"),
    ),
    path(
        "project/",
        include("sicop.project.urls"),
    ),
    path(
        "contract/",
        include("sicop.contract.urls"),
    ),
    path(
        "purchase_order/",
        include("sicop.purchase_order.urls"),
    ),
    path(
        "integration/",
        include("sicop.integration.urls"),
    ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handler
handler400 = custom_400
handler401 = custom_401
handler403 = custom_403
handler404 = custom_404
handler500 = custom_500
handler501 = custom_501
handler502 = custom_502
handler503 = custom_503

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
