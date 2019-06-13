from factory import DjangoModelFactory
from influencers.core.models import Category, SocialPlatform, Bank, Coupon


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category


class SocialPlatformFactory(DjangoModelFactory):
    class Meta:
        model = SocialPlatform


class BankFactory(DjangoModelFactory):
    class Meta:
        model = Bank


class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon
