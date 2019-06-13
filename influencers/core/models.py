import string
from django.db import models
from django.utils.crypto import get_random_string
from model_utils.models import TimeStampedModel
from auditlog.registry import auditlog
from partial_index import PartialIndex, PQ
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class Category(TimeStampedModel, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SocialPlatform(TimeStampedModel, SafeDeleteModel):
    """
    This represents a social media platform (Snapchat, Twitter, Facebook...etc.)
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bank(TimeStampedModel, SafeDeleteModel):
    """
    This represents a bank, currently being used for influencer payment data
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        indexes = [
            PartialIndex(
                fields=["swift", "deleted"], unique=True, where=PQ(deleted__isnull=True)
            )
        ]
        ordering = ["name"]

    name = models.CharField(max_length=50, blank=False)
    # https://en.wikipedia.org/wiki/ISO_9362
    swift = models.CharField(max_length=11, blank=False)

    def __str__(self):
        return self.name


class Coupon(TimeStampedModel):
    """
    Coupons are codes given to influencers to give customers a percentage discount on a
    given item.
    They also serve the purpose of tracking sales.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["code"]

    percentage = models.IntegerField(default=0)
    code = models.CharField(max_length=10)
    start = models.DateTimeField("start", null=True, blank=True)
    end = models.DateTimeField("end", null=True, blank=True)

    def __str__(self):
        return self.code

    def create_code(self):
        chars = get_random_string(length=4, allowed_chars=string.ascii_uppercase)
        nums = chars + str(self.percentage)
        return nums

    def save(self, *args, **kwargs):
        self.code = self.create_code()
        return super().save(*args, **kwargs)


auditlog.register(Bank)
auditlog.register(Category)
auditlog.register(Coupon)
auditlog.register(SocialPlatform)
