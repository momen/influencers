from datetime import date
from unittest.mock import MagicMock
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import Permission
from influencers.clients.tests.factories import (
    ClientFactory,
    OfferFactory,
    CampaignFactory,
    AssignedInfluencerFactory,
    InfluencerHistoryFactory,
    InfluencerPaymentFactory,
)
from influencers.core.tests.factories import (
    CategoryFactory,
    SocialPlatformFactory,
    BankFactory,
    CouponFactory,
)
from influencers.influencers.tests.factories import (
    InfluencerFactory,
    SocialAccountFactory,
)
from influencers.users.models import User
from influencers.taskapp.helpers import (
    get_assigned_influencers_unpaid,
    get_finance_has_permission_view_payment,
)


class GetAssignedInfluencersUnpaid(TestCase):
    """ Test get_assigned_influencers_unpaid function """

    def setUp(self):
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.category = CategoryFactory(name="Test category")
        self.client_obj = ClientFactory(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = OfferFactory(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.platform = SocialPlatformFactory(name="Test platform")
        self.bank = BankFactory(name="test2", swift="BEASUS33yyy")
        self.influencer = InfluencerFactory(
            name="influencer1",
            gender="MALE",
            category=self.category,
            phone="+201002896654",
            email="influencer@mail.com",
            bank=self.bank,
            IBAN="SA44 2000 0001",
            account_holder_name="influencer_",
        )
        self.social_account = SocialAccountFactory(
            username="social account1",
            platform=self.platform,
            influencer=self.influencer,
            cost=20.00,
        )
        self.campaign = CampaignFactory(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            cost_percentage=30.0,
            discount_percent=20.0,
        )
        self.coupoun = CouponFactory(percentage=20)
        self.assigned_influencer = AssignedInfluencerFactory(
            social_account=self.social_account,
            influencer=self.influencer,
            campaign=self.campaign,
            coupon=self.coupoun,
            billing="FIXED_COST",
            cost=20.0,
            discount=15,
            day=date.today(),
        )
        file_mock = MagicMock(spec="File", name="FileMock")
        self.influencer_payment = InfluencerPaymentFactory(
            assigned_influencer=self.assigned_influencer,
            day=date.today(),
            invoice=file_mock,
            billing_status="UNPAID",
        )

    def test_get_assigned_influencers_unpaid(self):
        assigned_influencers_unpaid_lst = get_assigned_influencers_unpaid()
        self.assertIsNotNone(assigned_influencers_unpaid_lst)
        self.assertIn(self.assigned_influencer, assigned_influencers_unpaid_lst)


class GetFinanceHasPermissionViewPayment(TestCase):
    """
    Test get_finance_has_permission_view_payment(),
    to get all email users has 'view_influencerpayment' permission
    """

    def setUp(self):
        self.perm = Permission.objects.get(codename="view_influencerpayment")
        self.user = User.objects.create(email="finance@mail.com", password="123")
        self.user.user_permissions.add(self.perm)

    def test_get_assigned_influencers_unpaid(self):
        email_lst = get_finance_has_permission_view_payment()
        self.assertIn(self.user.email, email_lst)
