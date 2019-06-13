from django.test import TestCase

from influencers.core.models import Category, SocialPlatform, Bank, Coupon
from influencers.core.tests.factories import (
    CategoryFactory,
    SocialPlatformFactory,
    BankFactory,
    CouponFactory,
)


class CategoryModelTestCase(TestCase):
    """ Test category model """

    def setUp(self):
        self.category = CategoryFactory(name="Test category")

    def test_model_can_create_category(self):
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.name, "Test category")

    def test_model_can_edit_category(self):
        self.category.name = "New category"
        self.category.save()
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "New category")


class SocialPlatformModelTestCase(TestCase):
    """ Test SocialPlatform model """

    def setUp(self):
        self.socialplatform = SocialPlatformFactory(name="Test socialplatform")

    def test_model_can_create_socialplatform(self):
        self.assertEqual(SocialPlatform.objects.count(), 1)
        self.assertEqual(self.socialplatform.name, "Test socialplatform")

    def test_model_can_edit_socialplatform(self):
        self.socialplatform.name = "New socialplatform"
        self.socialplatform.save()
        self.socialplatform.refresh_from_db()
        self.assertEqual(self.socialplatform.name, "New socialplatform")


class BankModelTestCase(TestCase):
    """ Test Bank model """

    def setUp(self):
        self.bank = BankFactory(name="Test bank", swift="BEASUS33xxx")

    def test_model_can_create_bank(self):
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(self.bank.name, "Test bank")
        self.assertEqual(self.bank.swift, "BEASUS33xxx")

    def test_model_can_edit_bank(self):
        self.bank.name = "New bank"
        self.bank.save()
        self.assertEqual(self.bank.name, "New bank")


class CouponModelTestCase(TestCase):
    """ Test Coupon model """

    def setUp(self):
        self.coupon = CouponFactory(percentage=20)

    def test_model_can_create_coupon(self):
        self.assertIsNotNone(self.coupon)
        self.assertEqual(Coupon.objects.count(), 1)
        self.assertEqual(self.coupon.percentage, 20)

    def test_model_can_edit_coupon(self):
        self.coupon.percentage = 50
        self.coupon.save()
        self.coupon.refresh_from_db()
        self.assertEqual(self.coupon.percentage, 50)
