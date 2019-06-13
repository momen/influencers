from datetime import date, timedelta

from django.contrib.auth.models import Permission
from django.db.models import Q

from influencers.clients.models import AssignedInfluencer
from influencers.users.models import User
from influencers.clients.models import InfluencerUnPaidNotification


def get_days_range_from_today(no_days=5):
    # 5 days before current date
    days_before = (date.today() - timedelta(days=no_days)).isoformat()
    # 5 days after current date
    days_after = (date.today() + timedelta(days=no_days)).isoformat()
    return days_before, days_after


def get_assigned_influencers_unpaid():
    """
    Get List of influencers assigned to a campaign and not yet paid
    or even cancel payment
    """
    days_before, days_after = get_days_range_from_today()
    assigned_influencers_unpaid_lst = (
        AssignedInfluencer.objects.filter(
            Q(influencer_payment__billing_status="UNPAID")
            | Q(influencer_payment__isnull=True)
        )
        .filter(day__range=[days_before, days_after])
        .all()
    )
    return assigned_influencers_unpaid_lst


def get_finance_has_permission_view_payment():
    """
    Get all email users has 'view_influencerpayment' permission
    """
    perm = Permission.objects.get(codename="view_influencerpayment")
    users = User.objects.filter(
        Q(groups__permissions=perm) | Q(user_permissions=perm)
    ).distinct()
    emails = [user.email for user in users]
    return emails


def save_assigned_influencers_unpaid():
    """
    save assigned influencers unpaid to InfluencerUnPaidNotification
    to notify finance gouplater
    """
    results_obj_lst = get_assigned_influencers_unpaid()
    for assign in results_obj_lst:
        found = InfluencerUnPaidNotification.objects.filter(
            influencer=assign.influencer, cost=assign.cost, day=assign.day
        ).exists()
        if not found:
            infl_not_paid = InfluencerUnPaidNotification(
                influencer=assign.influencer, cost=assign.cost, day=assign.day
            )
            infl_not_paid.save()
