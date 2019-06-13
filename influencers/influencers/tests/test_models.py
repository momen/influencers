from django.test import TestCase

from influencers.influencers.models import Influencer, SocialAccount
from influencers.influencers.tests.factories import (
    InfluencerFactory,
    SocialAccountFactory,
)
from influencers.core.tests.factories import CategoryFactory
from influencers.core.models import Category, SocialPlatform


class InfluencerModelTestCase(TestCase):
    """ Test influencer model """

    def setUp(self):
        self.category = CategoryFactory(name="Test category")
        self.influencer = InfluencerFactory(
            name="Test Influencer",
            gender="MALE",
            category=self.category,
            IBAN="SA44 2000 0001",
            account_holder_name="test",
        )

    def test_model_can_create_influencer(self):
        self.assertEqual(Influencer.objects.count(), 1)
        self.assertEqual(self.influencer.gender, "MALE")

    def test_model_can_edit_influencer(self):
        self.influencer.account_holder_name = "new"
        self.influencer.save()
        self.influencer.refresh_from_db()
        self.assertEqual(self.influencer.account_holder_name, "new")

    def test_model_influencer_ref_category(self):
        self.assertEqual(self.influencer.category, self.category)
        self.assertIsInstance(self.influencer.category, Category)


class SocialAccountModelTestCase(TestCase):
    """ Test SocialAccount model """

    def setUp(self):
        self.category = Category.objects.create(name="Test category")
        self.influencer = Influencer.objects.create(
            name="Test Influencer",
            gender="MALE",
            category=self.category,
            IBAN="SA44 2000 0001",
            account_holder_name="test",
        )
        self.socialplatform = SocialPlatform.objects.create(name="test2")
        self.social_account = SocialAccount.objects.create(
            username="socialaccount2",
            platform=self.socialplatform,
            influencer=self.influencer,
            cost=22,
        )

    def test_model_can_create_socialaccount(self):
        self.assertEqual(SocialAccount.objects.count(), 1)
        self.assertEqual(self.social_account.username, "socialaccount2")

    def test_model_edit_socialaccount(self):
        self.social_account.username = "new name"
        self.social_account.save()
        self.social_account.refresh_from_db()
        self.assertEqual(self.social_account.username, "new name")

    def test_model_socialaccount_ref_platform(self):
        self.assertEqual(self.social_account.platform, self.socialplatform)
        self.assertIsInstance(self.social_account.platform, SocialPlatform)

    def test_model_socialaccount_ref_influencer(self):
        self.assertEqual(self.social_account.influencer, self.influencer)
        self.assertIsInstance(self.social_account.influencer, Influencer)
