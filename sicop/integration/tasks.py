from celery import shared_task

from sicop.integration.utils.Xirux import XiruxIntegration


@shared_task
def update_from_xirux_task():
    xirux = XiruxIntegration()
    xirux.run()
