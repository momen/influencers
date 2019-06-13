from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    FloatField,
    PrimaryKeyRelatedField,
)
from influencers.clients.models import (
    Client,
    Offer,
    Campaign,
    AssignedInfluencer,
    InfluencerHistory,
    InfluencerPayment,
    InfluencerUnPaidNotification,
)


class CreateClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "name", "email", "account_manager", "phone")


class ClientSerializer(ModelSerializer):
    offer_count = SerializerMethodField()

    class Meta:
        model = Client
        depth = 1
        fields = ("id", "name", "email", "account_manager", "phone", "offer_count")

    def get_offer_count(self, obj):
        return obj.offers.count()


class CreateOfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ("id", "name", "client", "category", "billing")


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        depth = 1
        fields = ("id", "name", "client", "category", "billing")


class CreateCampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            "id",
            "offer",
            "account_manager",
            "cost_fixed",
            "cost_percentage",
            "discount_percent",
            "start",
            "end",
        )


class CampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign
        depth = 1
        fields = (
            "id",
            "offer",
            "account_manager",
            "cost_fixed",
            "cost_percentage",
            "discount_percent",
            "start",
            "end",
        )


class CreateAssignedInfluencerSerializer(ModelSerializer):
    class Meta:
        model = AssignedInfluencer
        fields = (
            "id",
            "social_account",
            "influencer",
            "campaign",
            "cost",
            "discount",
            "billing",
            "day",
        )


class AssignedInfluencerSerializer(ModelSerializer):
    total_raw_data = FloatField(read_only=True)
    total_validated_data = FloatField(read_only=True)

    class Meta:
        model = AssignedInfluencer
        depth = 1
        fields = (
            "id",
            "social_account",
            "influencer",
            "campaign",
            "cost",
            "coupon",
            "discount",
            "billing",
            "day",
            "total_raw_data",
            "total_validated_data",
        )


class CreateInfluencerHistorySerializer(ModelSerializer):
    class Meta:
        model = InfluencerHistory
        fields = ("id", "assigned_influencer", "data_type", "no_sales", "day_sales")


class UpdateInfluencerHistorySerializer(ModelSerializer):
    class Meta:
        model = InfluencerHistory
        fields = ("id", "data_type", "no_sales", "day_sales")


class InfluencerHistorySerializer(ModelSerializer):
    class Meta:
        model = InfluencerHistory
        depth = 1
        fields = ("id", "assigned_influencer", "data_type", "no_sales", "day_sales")


class InfluencerPaymentSerializer(ModelSerializer):
    class Meta:
        model = InfluencerPayment
        fields = ("id", "assigned_influencer", "day", "invoice", "billing_status")


class CalendarSerializer(ModelSerializer):
    offer_name = SerializerMethodField()
    influencer_payment = InfluencerPaymentSerializer()

    class Meta:
        model = AssignedInfluencer
        depth = 1
        fields = (
            "id",
            "influencer",
            "campaign",
            "day",
            "offer_name",
            "cost",
            "influencer_payment",
        )

    def get_offer_name(self, obj):
        return obj.campaign.offer.name

    def get_influencer_payment(self, obj):
        if hasattr(obj, "influencer_payment"):
            return obj.influencer_payment.all()
        else:
            return None


class CreateInfluencerUnPaidNotificationSerializer(ModelSerializer):
    class Meta:
        model = InfluencerUnPaidNotification
        fields = ("id", "influencer", "cost", "day")


class InfluencerUnPaidNotificationSerializer(ModelSerializer):
    influencer_name = SerializerMethodField()

    class Meta:
        model = InfluencerUnPaidNotification
        fields = ("id", "influencer_name", "cost", "day")

    def get_influencer_name(self, obj):
        return obj.influencer.name
