from django.db import models
from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField
from model_utils import Choices
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from auditlog.registry import auditlog
from partial_index import PartialIndex, PQ
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from influencers.core.models import SocialPlatform, Category, Bank


class Influencer(TimeStampedModel, SafeDeleteModel):
    """
    The basic building block of the system, influencers work on offers and get paid for their work.
    They also drive sales to a given product or service.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        indexes = [
            PartialIndex(
                fields=["IBAN", "deleted"], unique=True, where=PQ(deleted__isnull=True)
            )
        ]
        ordering = ["name"]

    GENDERS = Choices("MALE", "FEMALE")
    name = models.CharField(max_length=50)
    gender = StatusField(
        choices_name="GENDERS", blank=True, help_text="Choose between MALE, FEMALE"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="influencers",
        null=True,
        blank=True,
    )
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="influencers",
        null=True,
        blank=True,
    )
    # https://en.wikipedia.org/wiki/International_Bank_Account_Number
    IBAN = models.CharField(max_length=34)
    account_holder_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50, null=True)
    branch = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class SocialAccount(TimeStampedModel, SafeDeleteModel):
    """
    This represents an influencer's social media account
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["username"]

    username = models.CharField(max_length=50, blank=False)
    platform = models.ForeignKey(
        SocialPlatform, on_delete=models.CASCADE, related_name="accounts"
    )
    influencer = models.ForeignKey(
        Influencer, on_delete=models.CASCADE, related_name="accounts"
    )
    cost = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")

    def __str__(self):
        return self.username


auditlog.register(Influencer)
auditlog.register(SocialAccount)
