from django.core.management.base import BaseCommand
from influencers.taskapp.celery import save_notification_into_db


class Command(BaseCommand):
    """
    Run command 'python manage.py save_unpaid_influencers'
    to run task now of saving unpaid influencers to database to appear in notifications

    """

    help = "Save unpaid influencers into DB"

    def handle(self, *args, **kwargs):
        save_notification_into_db.apply_async()
