import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from influencers.users.tests.factories import UserFactory
from influencers.core.models import Category, SocialPlatform, Bank


class CategoryCreateAPITestCase(TestCase):
    """
    Test create a category and get category list
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("core:category-list")

    def test_create_category(self):
        category_data = {"name": "TestCatgory"}
        response = self.client.post(self.url, category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "TestCatgory")

    def test_list_category(self):
        Category.objects.create(name="test")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], Category.objects.count()
        )


class CategoryDetailAPITestCase(TestCase):
    """
    Test get, update, delete a category
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="test2")
        self.url = reverse("core:category-detail", kwargs={"pk": self.category.pk})

    def test_get_category(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.category)

    def test_update_category(self):
        new_data = {"name": "Something new"}
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Something new")

    def test_delete_category(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SocialplatformCreateAPITestCase(TestCase):
    """
    Test create a Socialplatform and get Social platform list
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("core:socialplatform-list")

    def test_create_category(self):
        socialplatform_data = {"name": "Test Socialplatform"}
        response = self.client.post(self.url, socialplatform_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SocialPlatform.objects.count(), 1)
        self.assertEqual(SocialPlatform.objects.get().name, "Test Socialplatform")

    def test_list_category(self):
        SocialPlatform.objects.create(name="test")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["count"], SocialPlatform.objects.count()
        )


class SocialplatformDetailAPITestCase(TestCase):
    """
    Test get, update, delete a social platform
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.socialplatform = SocialPlatform.objects.create(name="test2")
        self.url = reverse(
            "core:socialplatform-detail", kwargs={"pk": self.socialplatform.pk}
        )

    def test_get_socialplatform(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.socialplatform)

    def test_update_category(self):
        new_data = {"name": "Something new"}
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Something new")

    def test_delete_category(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BankCreateAPITestCase(TestCase):
    """
    Test create a bank and get banks list
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("core:bank-list")

    def test_create_bank(self):
        bank_data = {"name": "Test bank", "swift": "BEASUS33xxx"}
        response = self.client.post(self.url, bank_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(Bank.objects.get().name, "Test bank")
        self.assertEqual(Bank.objects.get().swift, "BEASUS33xxx")

    def test_list_bank(self):
        Bank.objects.create(name="test", swift="BEASUS33xxx")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["count"], Bank.objects.count())


class BankDetailAPITestCase(TestCase):
    """
    Test get, update, delete a bank account
    """

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.bank = Bank.objects.create(name="test2", swift="BEASUS33xxx")
        self.url = reverse("core:bank-detail", kwargs={"pk": self.bank.pk})

    def test_get_bank(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.bank)

    def test_update_bank(self):
        new_data = {"name": "New bank", "swift": "BEASUS33yyy"}
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "New bank")

    def test_delete_bank(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_after_delete(self):
        self.client.delete(self.url)
        bank_data = {"name": "Test bank", "swift": "BEASUS33xxx"}
        response = self.client.post(reverse("core:bank-list"), bank_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
