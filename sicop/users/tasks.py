from config import celery_app


@celery_app.task()
def test():
    """A pointless Celery task to demonstrate usage."""
    return True
