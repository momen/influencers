from django.test import TestCase
from influencers.clients.models import (
    Client,
    Offer,
    Campaign,
    AssignedInfluencer,
    InfluencerHistory,
)
from influencers.influencers.models import Influencer, SocialAccount
from influencers.core.models import Coupon, Category
from influencers.users.models import User
from influencers.clients.tests.factories import (
    ClientFactory,
    OfferFactory,
    CampaignFactory,
    AssignedInfluencerFactory,
    InfluencerHistoryFactory,
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


class ClientModelTestCase(TestCase):
    """ Test client model """

    def setUp(self):
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = ClientFactory(
            name="Test client", account_manager=self.account_manager
        )

    def test_model_can_create_client(self):
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(self.client.name, "Test client")

    def test_model_can_edit_client(self):
        self.client.name = "New client"
        self.client.save()
        self.client.refresh_from_db()
        self.assertEqual(self.client.name, "New client")

    def test_model_can_edit_client_reference_acc_manager(self):
        self.assertEqual(self.client.account_manager, self.account_manager)
        self.assertIsInstance(self.client.account_manager, User)


class OfferModelTestCase(TestCase):
    """ Test offer model """

    def setUp(self):
        self.category = CategoryFactory(name="test")
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = ClientFactory(
            name="Test client", account_manager=self.account_manager
        )
        self.offer = OfferFactory(
            name="Test offer",
            client=self.client,
            category=self.category,
            billing="REVENUE_SHARE",
        )

    def test_model_can_create_offer(self):
        self.assertEqual(Offer.objects.count(), 1)
        self.assertIsInstance(self.offer, Offer)
        self.assertEqual(self.offer.name, "Test offer")
        self.assertEqual(self.offer.billing, "REVENUE_SHARE")

    def test_model_can_edit_offer(self):
        self.offer.name = "New offer"
        self.offer.billing = "FIXED_PRICE"
        self.offer.save()
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.name, "New offer")
        self.assertEqual(self.offer.billing, "FIXED_PRICE")

    def test_model_offer_ref_client(self):
        self.assertEqual(self.offer.client, self.client)
        self.assertIsInstance(self.offer.client, Client)

    def test_model_offer_ref_category(self):
        self.assertEqual(self.offer.category, self.category)
        self.assertIsInstance(self.offer.category, Category)


class CampaignModelTestCase(TestCase):
    """ Test campaign model """

    def setUp(self):
        self.category = CategoryFactory(name="test")
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = ClientFactory(
            name="Test client", account_manager=self.account_manager
        )
        self.offer = OfferFactory(
            name="Test offer",
            client=self.client,
            category=self.category,
            billing="REVENUE_SHARE",
        )
        self.campaign = CampaignFactory(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            discount_percent=30.0,
        )

    def test_model_can_create_campaign(self):
        self.assertEqual(Campaign.objects.count(), 1)
        self.assertIsInstance(self.campaign, Campaign)

    def test_model_can_edit_campaign(self):
        self.campaign.cost_fixed = 30.0
        self.campaign.discount_percent = 40.0
        self.campaign.save()
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.cost_fixed, 30.0)
        self.assertEqual(self.campaign.discount_percent, 40.0)

    def test_model_campaign_ref_offer(self):
        self.assertEqual(self.campaign.offer, self.offer)
        self.assertIsInstance(self.campaign.offer, Offer)

    def test_model_campaign_ref_acc_manager(self):
        self.assertEqual(self.campaign.account_manager, self.account_manager)
        self.assertIsInstance(self.campaign.account_manager, User)


class AssignedInfluencerModelTestCase(TestCase):
    """ Test AssignedInfluencer model """

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
            day="2018-11-11",
        )

    def test_model_can_create_assignedinfluencer(self):
        self.assertEqual(AssignedInfluencer.objects.count(), 1)
        self.assertEqual(self.assigned_influencer.billing, "FIXED_COST")
        self.assertIsInstance(self.assigned_influencer, AssignedInfluencer)

    def test_model_can_edit_assignedinfluencer(self):
        self.assigned_influencer.billing = "REVENUE_SHARE_PERCENTAGE"
        self.assigned_influencer.cost = 30.0
        self.assigned_influencer.discount = 20
        self.assigned_influencer.save()
        self.assigned_influencer.refresh_from_db()
        self.assertEqual(self.assigned_influencer.billing, "REVENUE_SHARE_PERCENTAGE")
        self.assertEqual(self.assigned_influencer.cost, 30.0)
        self.assertEqual(self.assigned_influencer.discount, 20)

    def test_model_assignedinfluencer_reference_campaign(self):
        self.assertEqual(self.assigned_influencer.campaign, self.campaign)
        self.assertIsInstance(self.assigned_influencer.campaign, Campaign)

    def test_model_assignedinfluencer_reference_coupon(self):
        self.assertEqual(self.assigned_influencer.coupon, self.coupoun)
        self.assertIsInstance(self.assigned_influencer.coupon, Coupon)

    def test_model_assignedinfluencer_reference_influencer(self):
        self.assertEqual(self.assigned_influencer.influencer, self.influencer)
        self.assertIsInstance(self.assigned_influencer.influencer, Influencer)

    def test_model_assignedinfluencer_reference_social_account(self):
        self.assertEqual(self.assigned_influencer.social_account, self.social_account)
        self.assertIsInstance(self.assigned_influencer.social_account, SocialAccount)


class InfluencerHistoryModelTestCase(TestCase):
    """ Test InfluencerHistory model """

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
            day="2018-11-11",
        )
        self.influencer_history = InfluencerHistoryFactory(
            data_type="RAW_DATA",
            assigned_influencer=self.assigned_influencer,
            no_sales=300.0,
            day_sales="2018-11-11",
        )

    def test_model_can_create_influencer_history(self):
        self.assertEqual(InfluencerHistory.objects.count(), 1)
        self.assertIsNotNone(self.influencer_history)
        self.assertEqual(self.influencer_history.data_type, "RAW_DATA")
        self.assertEqual(self.influencer_history.no_sales, 300.0)
        self.assertIsInstance(self.influencer_history, InfluencerHistory)

    def test_model_can_edit_influencer_history(self):
        self.influencer_history.data_type = "VALIDATED_DATA"
        self.influencer_history.no_sales = 200.0
        self.influencer_history.save()
        self.influencer_history.refresh_from_db()
        self.assertEqual(self.influencer_history.data_type, "VALIDATED_DATA")
        self.assertEqual(self.influencer_history.no_sales, 200.0)

    def test_model_influencer_history_referenced_assigendinfluencer(self):
        self.assertIsInstance(
            self.influencer_history.assigned_influencer, AssignedInfluencer
        )
        self.assertEqual(
            self.influencer_history.assigned_influencer, self.assigned_influencer
        )
