from django.test import TestCase

from influencers.users.models import User
from influencers.users.tests.factories import UserFactory


class UserModelTestCase(TestCase):
    """ Test User Model """

    def setUp(self):
        self.user = UserFactory(email="test_user@mail.com", password="123")

    def test_model_can_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, "test_user@mail.com")

    def test_model_can_edit_user(self):
        self.user.email = "new_test_user@mail.com"
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new_test_user@mail.com")
