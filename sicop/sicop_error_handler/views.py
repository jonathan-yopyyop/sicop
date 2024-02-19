# en views.py de tu aplicación
from django.shortcuts import render


def custom_400(request, exception):
    print(exception)
    template_name = "sicop/frontend/sicop_error_handler/400.html"
    return render(request, template_name)


def custom_401(request, exception):
    print(exception)
    template_name = "sicop/frontend/sicop_error_handler/401.html"
    return render(request, template_name)


def custom_403(request, exception):
    print(exception)
    template_name = "sicop/frontend/sicop_error_handler/403.html"
    return render(request, template_name)


def custom_404(request, exception):
    template_name = "sicop/frontend/sicop_error_handler/404.html"
    return render(request, template_name, status=404)


def custom_500(request):
    template_name = "sicop/frontend/sicop_error_handler/500.html"
    return render(request, template_name)


def custom_501(request, exception):
    print(exception)
    template_name = "sicop/frontend/sicop_error_handler/501.html"
    return render(request, template_name)


def custom_502(request, exception):
    print(exception)
    template_name = "sicop/frontend/sicop_error_handler/502.html"
    return render(request, template_name)


def custom_503(request, exception):
    print(exception)
    template_name = "sicop/frontend/sicop_error_handler/503.html"
    return render(request, template_name)
