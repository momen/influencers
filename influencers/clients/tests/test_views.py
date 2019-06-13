import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from influencers.users.tests.factories import UserFactory
from influencers.users.models import User
from influencers.influencers.models import Influencer, SocialAccount
from influencers.core.models import Category, Bank, Coupon, SocialPlatform
from influencers.clients.models import (
    Client,
    Offer,
    Campaign,
    AssignedInfluencer,
    InfluencerHistory,
)


class ClientCreateAPITestCase(TestCase):
    """
    Test create a client and get his clients list (his clients list)
    """

    def setUp(self):
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.account_manager)
        self.url = reverse("clients:client-list")

    def test_create_client(self):
        client_data = {
            "name": "Test client",
            "email": "test@mail.com",
            "account_manager": self.account_manager.id,
            "phone": "+201002896457",
        }
        response = self.client.post(self.url, client_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().name, "Test client")
        self.assertEqual(Client.objects.get().email, "test@mail.com")

    def test_list_client(self):
        Client.objects.create(
            name="Test1",
            email="test1@mail.com",
            account_manager=self.account_manager,
            phone="+201002896812",
        )
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)["count"] == Client.objects.count())


class ClientDetailAPITestCase(TestCase):
    """
    Test get, update, delete a client (only his clients)
    """

    def setUp(self):
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.account_manager)
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.url = reverse("clients:client-detail", kwargs={"pk": self.client_obj.pk})

    def test_get_client(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.client_obj)

    def test_update_client(self):
        new_data = {
            "name": "New client",
            "email": "new_client@mail.com",
            "account_manager": self.account_manager.id,
            "phone": "+201002896321",
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "New client")

    def test_delete_client(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ClientOfferListAPITestCase(TestCase):
    """ Test client offers list only """

    def setUp(self):
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.account_manager)

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.url = reverse("clients:client-offers", kwargs={"id": self.client_obj.id})

    def test_list_client_offers(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            json.loads(response.content)["count"]
            == Offer.objects.filter(client__id=self.client_obj.id).count()
        )


class OffersCreateAPITestCase(TestCase):
    """ Test offers list (his offers list) and create offer object """

    def setUp(self):
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.account_manager)

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.url = reverse("clients:offer-list")

    def test_create_offer(self):
        offer_data = {
            "name": "Test offer",
            "client": self.client_obj.id,
            "category": self.category.id,
            "billing": "FIXED_PRICE",
        }
        response = self.client.post(self.url, offer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(Offer.objects.get().name, "Test offer")
        self.assertEqual(Offer.objects.get().billing, "FIXED_PRICE")

    def test_list_offers(self):
        Offer.objects.create(
            name="offer1",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)["count"] == Offer.objects.count())


class OfferDetailAPITestCase(TestCase):
    """
    Test get, update, delete an offer
    """

    def setUp(self):
        self.client = APIClient()
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client.force_authenticate(user=self.account_manager)

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.url = reverse("clients:offer-detail", kwargs={"pk": self.offer.pk})

    def test_get_offer(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.offer)

    def test_update_offer(self):
        new_data = {
            "name": "New offer",
            "client": self.client_obj.id,
            "category": self.category.id,
            "billing": "REVENUE_SHARE",
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "New offer")

    def test_delete_offer(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CampaignCreateAPITestCase(TestCase):
    """
    Test create a campaign and get campaigns list
    """

    def setUp(self):
        self.client = APIClient()
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client.force_authenticate(user=self.account_manager)
        self.url = reverse("clients:campaign-list")

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )

    def test_create_campaign(self):

        campaign_data = {
            "offer": self.offer.id,
            "account_manager": self.account_manager.id,
            "cost_fixed": 20.0,
            "discount_percent": 30.0,
        }
        response = self.client.post(self.url, campaign_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(Campaign.objects.get().cost_fixed, 20.0)
        self.assertEqual(Campaign.objects.get().discount_percent, 30.0)

    def test_list_campaign(self):
        Campaign.objects.create(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            discount_percent=30.0,
        )
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], Campaign.objects.count()
        )


class CampaignDetailAPITestCase(TestCase):
    """
    Test get, update, delete a campaign (account manager campaigns)
    """

    def setUp(self):
        self.client = APIClient()
        self.account_manager = User.objects.create(email="account_manager@mail.com")
        self.client.force_authenticate(user=self.account_manager)

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.campaign = Campaign.objects.create(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            discount_percent=30.0,
        )
        self.url = reverse("clients:campaign-detail", kwargs={"pk": self.campaign.pk})

    def test_get_campaign(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.campaign.offer)

    def test_update_campaign(self):
        new_data = {
            "offer": self.offer.id,
            "account_manager": self.account_manager.id,
            "cost_fixed": 20.0,
            "discount_percent": 30.0,
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "30.0")

    def test_delete_campaign(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AssignedInfluencerCreateAPITestCase(TestCase):
    """
    Test create an assigned influencers to a campaign
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.account_manager = User.objects.create(email="account_manager@mail.com")

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.platform = SocialPlatform.objects.create(name="Test platform")
        self.bank = Bank.objects.create(name="test2", swift="BEASUS33yyy")
        self.influencer = Influencer.objects.create(
            name="influencer1",
            gender="MALE",
            category=self.category,
            phone="+201002896654",
            email="influencer@mail.com",
            bank=self.bank,
            IBAN="SA44 2000 0001",
            account_holder_name="influencer_",
        )
        self.social_account = SocialAccount.objects.create(
            username="social account1",
            platform=self.platform,
            influencer=self.influencer,
            cost=20.00,
        )
        self.campaign = Campaign.objects.create(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            cost_percentage=30.0,
            discount_percent=20.0,
        )

        self.coupoun = Coupon.objects.create(percentage=20)
        self.url = reverse(
            "clients:assign-influencers-list", kwargs={"id": self.campaign.id}
        )

    def test_create_assignedinfluencer_record(self):

        assignedinfluencer_data = {
            "social_account": self.social_account.id,
            "influencer": self.influencer.id,
            "campaign": self.campaign.id,
            "coupon": self.coupoun.id,
            "billing": "FIXED_COST",
            "cost": 20.0,
            "discount": 15,
            "day": "2018-11-11",
        }
        response = self.client.post(self.url, assignedinfluencer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssignedInfluencer.objects.count(), 1)
        self.assertEqual(AssignedInfluencer.objects.get().billing, "FIXED_COST")
        self.assertEqual(AssignedInfluencer.objects.get().discount, 15)

    def test_list_assignedinfluencer(self):
        AssignedInfluencer.objects.create(
            social_account=self.social_account,
            influencer=self.influencer,
            campaign=self.campaign,
            coupon=self.coupoun,
            billing="FIXED_COST",
            cost=20.0,
            discount=15,
            day="2018-11-11",
        )

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], AssignedInfluencer.objects.count()
        )


class AssignedInfluencerDetailAPITestCase(TestCase):
    """
    Test get, update, delete assigned influencers to a campaign
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.account_manager = User.objects.create(email="account_manager@mail.com")

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="client1",
            email="client1@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.platform = SocialPlatform.objects.create(name="Test platform")
        self.bank = Bank.objects.create(name="test2", swift="BEASUS33yyy")
        self.influencer = Influencer.objects.create(
            name="influencer1",
            gender="MALE",
            category=self.category,
            phone="+201002896654",
            email="influencer@mail.com",
            bank=self.bank,
            IBAN="SA44 2000 0001",
            account_holder_name="influencer_",
        )
        self.social_account = SocialAccount.objects.create(
            username="social account1",
            platform=self.platform,
            influencer=self.influencer,
            cost=20.00,
        )
        self.campaign = Campaign.objects.create(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            cost_percentage=30.0,
            discount_percent=20.0,
        )

        self.coupoun = Coupon.objects.create(percentage=20)
        self.assignedinfluencer = AssignedInfluencer.objects.create(
            social_account=self.social_account,
            influencer=self.influencer,
            campaign=self.campaign,
            coupon=self.coupoun,
            billing="FIXED_COST",
            cost=20.0,
            discount=15,
            day="2018-11-11",
        )

        self.url = reverse(
            "clients:assign-influencers-detail",
            kwargs={"id": self.assignedinfluencer.id},
        )

    def test_get_assigned_influencer(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.assignedinfluencer.influencer)
        self.assertContains(response, self.assignedinfluencer.coupon)

    def test_update_assigned_influencer(self):
        new_data = {
            "social_account": self.social_account.id,
            "influencer": self.influencer.id,
            "campaign": self.campaign.id,
            "coupon": self.coupoun.id,
            "billing": "REVENUE_SHARE_PERCENTAGE",
            "cost": 20.0,
            "discount": 50,
            "day": "2018-11-11",
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "REVENUE_SHARE_PERCENTAGE")

    def test_delete_assigned_influencer(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class InfluencerHistoryCreateAPITestCase(TestCase):
    """
    Test create an influencer history to a campaign(influencer adding numbers of sales using his coupoun)
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.account_manager = User.objects.create(email="account_manager@mail.com")

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.platform = SocialPlatform.objects.create(name="Test platform")
        self.bank = Bank.objects.create(name="test2", swift="BEASUS33yyy")
        self.influencer = Influencer.objects.create(
            name="influencer1",
            gender="MALE",
            category=self.category,
            phone="+201002896654",
            email="influencer@mail.com",
            bank=self.bank,
            IBAN="SA44 2000 0001",
            account_holder_name="influencer_",
        )
        self.social_account = SocialAccount.objects.create(
            username="social account1",
            platform=self.platform,
            influencer=self.influencer,
            cost=20.00,
        )
        self.campaign = Campaign.objects.create(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            cost_percentage=30.0,
            discount_percent=20.0,
        )

        self.coupoun = Coupon.objects.create(percentage=20)
        self.assigned_influencer = AssignedInfluencer.objects.create(
            social_account=self.social_account,
            influencer=self.influencer,
            campaign=self.campaign,
            coupon=self.coupoun,
            billing="FIXED_COST",
            cost=20.0,
            discount=15,
            day="2018-11-11",
        )
        self.url = reverse(
            "clients:influencer-history-list",
            kwargs={"id": self.assigned_influencer.id},
        )

    def test_create_influencer_history(self):

        influencer_history_data = {
            "data_type": "RAW_DATA",
            "assigned_influencer": self.assigned_influencer.id,
            "no_sales": 250.0,
            "day_sales": "2018-11-11",
        }
        response = self.client.post(self.url, influencer_history_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InfluencerHistory.objects.count(), 1)
        self.assertEqual(InfluencerHistory.objects.get().data_type, "RAW_DATA")
        self.assertEqual(InfluencerHistory.objects.get().no_sales, 250.0)

    def test_list_influencer_history(self):
        InfluencerHistory.objects.create(
            data_type="RAW_DATA",
            assigned_influencer=self.assigned_influencer,
            no_sales=300.0,
            day_sales="2018-11-11",
        )

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], InfluencerHistory.objects.count()
        )


class InfluencerHistoryDetailAPITestCase(TestCase):
    """
    Test get, update, delete an influencer history to a campaign(influencer adding numbers of sales using his coupoun)
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.account_manager = User.objects.create(email="account_manager@mail.com")

        self.category = Category.objects.create(name="Test category")
        self.client_obj = Client.objects.create(
            name="Test client",
            email="test_client@mail.com",
            account_manager=self.account_manager,
            phone="+201002896457",
        )
        self.offer = Offer.objects.create(
            name="Test offer",
            client=self.client_obj,
            category=self.category,
            billing="FIXED_PRICE",
        )
        self.platform = SocialPlatform.objects.create(name="Test platform")
        self.bank = Bank.objects.create(name="test2", swift="BEASUS33yyy")
        self.influencer = Influencer.objects.create(
            name="influencer1",
            gender="MALE",
            category=self.category,
            phone="+201002896654",
            email="influencer@mail.com",
            bank=self.bank,
            IBAN="SA44 2000 0001",
            account_holder_name="influencer_",
        )
        self.social_account = SocialAccount.objects.create(
            username="social account1",
            platform=self.platform,
            influencer=self.influencer,
            cost=20.00,
        )
        self.campaign = Campaign.objects.create(
            offer=self.offer,
            account_manager=self.account_manager,
            cost_fixed=20.0,
            cost_percentage=30.0,
            discount_percent=20.0,
        )

        self.coupoun = Coupon.objects.create(percentage=20)
        self.assigned_influencer = AssignedInfluencer.objects.create(
            social_account=self.social_account,
            influencer=self.influencer,
            campaign=self.campaign,
            coupon=self.coupoun,
            billing="FIXED_COST",
            cost=20.0,
            discount=15,
            day="2018-11-11",
        )
        self.influencer_history = InfluencerHistory.objects.create(
            data_type="RAW_DATA",
            assigned_influencer=self.assigned_influencer,
            no_sales=300.0,
            day_sales="2018-11-11",
        )
        self.url = reverse(
            "clients:influencer-history-detail",
            kwargs={"id": self.influencer_history.id},
        )

    def test_get_influencer_history(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.influencer_history.no_sales)
        self.assertContains(response, self.influencer_history.data_type)

    def test_update_influencer_history(self):
        new_data = {
            "data_type": "VALIDATED_DATA",
            "assigned_influencer": self.assigned_influencer.id,
            "no_sales": 600.0,
            "day_sales": "2018-11-12",
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "VALIDATED_DATA")

    def test_delete_influencer_history(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
