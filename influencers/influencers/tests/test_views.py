import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from influencers.influencers.models import Influencer, SocialAccount
from influencers.users.tests.factories import UserFactory
from influencers.core.models import Category, SocialPlatform


class InfluencerCreateAPITestCase(TestCase):
    """
    Test create a influnencer and get influencer list
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("influencers:influencer-list")
        self.category = Category.objects.create(name="Test category")

    def test_create_influencer(self):
        influencer_data = {
            "name": "Test Influencer",
            "gender": "MALE",
            "category": self.category.id,
            "IBAN": "SA44 2000 0001",
            "account_holder_name": "test",
        }
        response = self.client.post(self.url, influencer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Influencer.objects.count(), 1)
        self.assertEqual(Influencer.objects.get().name, "Test Influencer")

    def test_list_influencers(self):
        Influencer.objects.create(
            name="Test Influencer",
            gender="MALE",
            category=self.category,
            IBAN="SA44 2000 0001",
            account_holder_name="test",
        )

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], Influencer.objects.count()
        )


class InfluencerDetailAPITestCase(TestCase):
    """
    Test get, update, delete an influencer
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Test category")
        self.influencer = Influencer.objects.create(
            name="Test Influencer",
            gender="MALE",
            category=self.category,
            IBAN="SA44 2000 0001",
            account_holder_name="test",
        )
        self.url = reverse(
            "influencers:influencer-detail", kwargs={"pk": self.influencer.pk}
        )

    def test_get_influencer(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.influencer)

    def test_update_influencer(self):
        new_data = {
            "name": "New Influencer",
            "gender": "MALE",
            "category": self.category.id,
            "IBAN": "SA44 2000 0001",
            "account_holder_name": "test",
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "New Influencer")

    def test_delete_influencer(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_after_delete(self):
        self.client.delete(self.url)
        influencer_data = {
            "name": "New Influencer",
            "gender": "MALE",
            "category": self.category.id,
            "IBAN": "SA44 2000 0001",
            "account_holder_name": "test",
        }
        response = self.client.post(
            reverse("influencers:influencer-list"), influencer_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SocialAccountCreateAPITestCase(TestCase):
    """
    Test create a socialaccount and get socialaccount list
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("influencers:socialaccount-list")
        self.category = Category.objects.create(name="Test category")
        self.influencer = Influencer.objects.create(
            name="Test Influencer",
            gender="MALE",
            category=self.category,
            IBAN="SA44 2000 0001",
            account_holder_name="test",
        )
        self.socialplatform = SocialPlatform.objects.create(name="test2")

    def test_create_socialaccount(self):
        socialaccount_data = {
            "username": "socialaccount1",
            "platform": self.socialplatform.id,
            "influencer": self.influencer.id,
            "cost": 22,
        }
        response = self.client.post(self.url, socialaccount_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SocialAccount.objects.count(), 1)
        self.assertEqual(SocialAccount.objects.get().username, "socialaccount1")

    def test_list_socialaccounts(self):
        SocialAccount.objects.create(
            username="socialaccount2",
            platform=self.socialplatform,
            influencer=self.influencer,
            cost=22,
        )

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], SocialAccount.objects.count()
        )


class SocialAccountDetailAPITestCase(TestCase):
    """
    Test get, update, delete a social account
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Test category")
        self.influencer = Influencer.objects.create(
            name="Test Influencer",
            gender="MALE",
            category=self.category,
            IBAN="SA44 2000 0001",
            account_holder_name="test",
        )
        self.socialplatform = SocialPlatform.objects.create(name="test2")
        self.socialaccount = SocialAccount.objects.create(
            username="socialaccount2",
            platform=self.socialplatform,
            influencer=self.influencer,
            cost=22.5,
        )
        self.url = reverse(
            "influencers:socialaccount-detail", kwargs={"pk": self.socialaccount.pk}
        )

    def test_get_socialaccount(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.socialaccount)

    def test_update_socialaccount(self):
        new_data = {
            "username": "New socialaccount",
            "platform": self.socialplatform.id,
            "influencer": self.influencer.id,
            "cost": 33.0,
        }
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "New socialaccount")

    def test_delete_socialaccount(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
