import os
from django.apps import AppConfig
from django.conf import settings
from django.core.mail import send_mail
from celery import Celery
from celery.schedules import crontab


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.local"
    )  # pragma: no cover


app = Celery("influencers")


class CeleryAppConfig(AppConfig):
    name = "influencers.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.
        app.config_from_object("django.conf:settings", namespace="CELERY")
        app.autodiscover_tasks()


@app.task
def send_mail_to_finance():
    """ Send mail to finance team Influencers unpaid at 9 am every day"""
    from .helpers import (
        get_assigned_influencers_unpaid,
        get_finance_has_permission_view_payment,
    )  # noqa  #import here to avoid issue

    results_obj_lst = get_assigned_influencers_unpaid()
    finance_recipients = get_finance_has_permission_view_payment()
    if results_obj_lst:
        results_str_lst = [str(r) for r in results_obj_lst]
        body_str = "\n".join(results_str_lst)
        send_mail(
            "Influencers not paid",
            body_str,
            "techops@arabyads.com",
            finance_recipients,
            fail_silently=False,
        )


@app.task
def save_notification_into_db():
    """
    Save unpaid AssignedInflunecers into
    InfluencerUnPaidNotification table at 9 am every day
    """
    from .helpers import save_assigned_influencers_unpaid  # noqa

    save_assigned_influencers_unpaid()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every day morning at 9 a.m.
    sender.add_periodic_task(crontab(hour=9, minute=0), send_mail_to_finance)
    sender.add_periodic_task(crontab(hour=9, minute=0), save_notification_into_db)
