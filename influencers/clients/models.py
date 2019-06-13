from django.db import models
from django.db.models import Sum
from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField
from auditlog.registry import auditlog
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from influencers.users.models import User
from influencers.core.models import Category, Coupon
from influencers.influencers.models import Influencer, SocialAccount


class Client(TimeStampedModel, SafeDeleteModel):
    """
    Clients provide offers for influencers to work on
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=True)
    account_manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="clients"
    )
    phone = PhoneNumberField()

    def __str__(self):
        return self.name


class Offer(TimeStampedModel, SafeDeleteModel):
    """
    An offer is a marketing opportunity made by the client
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=50, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="offers")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="offers"
    )
    BILLING_TYPE = Choices("FIXED_PRICE", "REVENUE_SHARE", "AGENCY")
    billing = StatusField(
        choices_name="BILLING_TYPE",
        blank=False,
        help_text="Choose from FIXED_PRICE, REVENUE_SHARE, AGENCY",
    )

    def __str__(self):
        return self.name


class Campaign(TimeStampedModel, SafeDeleteModel):
    """
    Represents a time period in an offer
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["-start"]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="campaigns")
    account_manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="campaigns"
    )
    cost_fixed = models.FloatField(default=0.0)
    cost_percentage = models.FloatField(default=0.0)
    discount_percent = models.FloatField(default=0.0)
    start = models.DateTimeField("start", null=True, blank=True)
    end = models.DateTimeField("end", null=True, blank=True)

    def __str__(self):
        return "Campaign for {} from {} to {}".format(self.offer, self.start, self.end)


class AssignedInfluencer(TimeStampedModel, SafeDeleteModel):
    """
    This represents assigned influencers to a campaign
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ["influencer"]

    social_account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="assigned_influencer"
    )
    influencer = models.ForeignKey(
        Influencer, on_delete=models.CASCADE, related_name="assigned_influencer"
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="assigned_influencer"
    )
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="assigned_influencer"
    )
    # REVENUE_SHARE_FIXED->percentage per Item, REVENUE_SHARE_PERCENTAGE->percentage per Total revenue
    BILLING_TYPE = Choices(
        "FIXED_COST", "REVENUE_SHARE_FIXED", "REVENUE_SHARE_PERCENTAGE"
    )
    billing = StatusField(
        choices_name="BILLING_TYPE",
        blank=False,
        null=False,
        help_text="Choose between FIXED_COST, REVENUE_SHARE_FIXED, REVENUE_SHARE_PERCENTAGE",
    )
    cost = models.FloatField(default=0.0)
    discount = models.IntegerField(default=0)
    day = models.DateField(blank=False, null=False)

    @property
    def total_raw_data(self):
        query = self.history.filter(data_type="RAW_DATA")
        aggregation = query.aggregate(total_raw_data=Sum("no_sales"))
        result = aggregation.get("total_raw_data")
        return result or 0.0

    @property
    def total_validated_data(self):
        query = self.history.filter(data_type="VALIDATED_DATA")
        aggregation = query.aggregate(total_validated_data=Sum("no_sales"))
        result = aggregation.get("total_validated_data")
        return result or 0.0

    def __str__(self):
        return "{} should be received {} before {}".format(
            self.influencer, self.cost, self.day
        )


class InfluencerHistory(TimeStampedModel, SafeDeleteModel):
    """
    This is represents influencer adding numbers of sales using his coupoun
    data of number of sales are raw_data(to be achieved) or validated_data(already achieved/final)
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    DATA_TYPES = Choices("RAW_DATA", "VALIDATED_DATA")
    data_type = StatusField(
        choices_name="DATA_TYPES", help_text="Choose between RAW DATA, VALIDATED DATA"
    )
    assigned_influencer = models.ForeignKey(
        AssignedInfluencer, on_delete=models.CASCADE, related_name="history"
    )
    no_sales = models.FloatField(default=0.0)
    day_sales = models.DateField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Influencer histories"
        ordering = ["assigned_influencer"]

    def __str__(self):
        return "No sales {} on {}".format(self.no_sales, self.day_sales)


class InfluencerPayment(TimeStampedModel, SafeDeleteModel):
    """ An InfluencerPayment is payment record to campaign assigned to influencer by an accountant """

    _safedelete_policy = SOFT_DELETE_CASCADE
    assigned_influencer = models.OneToOneField(
        AssignedInfluencer, on_delete=models.CASCADE, related_name="influencer_payment"
    )
    day = models.DateField(blank=False, null=False)
    invoice = models.FileField(
        blank=False, null=False, default="", upload_to="invoices/"
    )

    BILLING_STATUS = Choices("UNPAID", "PAID")
    billing_status = StatusField(choices_name="BILLING_STATUS", blank=False, null=False)

    def __str__(self):
        return "Payment to {} on {}".format(self.assigned_influencer, self.day)


class InfluencerUnPaidNotification(TimeStampedModel, SafeDeleteModel):
    """ Influencers list not paid notifications that shoud sent to finance group"""

    _safedelete_policy = SOFT_DELETE_CASCADE
    influencer = models.ForeignKey(
        Influencer, on_delete=models.CASCADE, related_name="influencer_notification"
    )
    cost = models.FloatField(default=0.0)
    day = models.DateField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Influencer upaid notifications"
        ordering = ["influencer"]

    def __str__(self):
        return "Influencer {} costs {} on {}".format(
            self.influencer, self.cost, self.day
        )


auditlog.register(AssignedInfluencer)
auditlog.register(Campaign)
auditlog.register(Client)
auditlog.register(InfluencerHistory)
auditlog.register(Offer)
auditlog.register(InfluencerPayment)
auditlog.register(InfluencerUnPaidNotification)
