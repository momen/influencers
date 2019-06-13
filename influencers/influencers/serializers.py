from rest_framework.serializers import ModelSerializer, ValidationError
from django.db.utils import IntegrityError
from .models import Influencer, SocialAccount


class CreateInfluencerSerializer(ModelSerializer):
    class Meta:
        model = Influencer
        fields = (
            "id",
            "name",
            "gender",
            "category",
            "phone",
            "email",
            "bank",
            "IBAN",
            "account_holder_name",
            "city",
            "branch",
        )

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            return instance
        except IntegrityError:
            raise ValidationError(
                {"swift": [u"Influencer with this IBAN already exists."]}
            )


class InfluencerSerializer(ModelSerializer):
    class Meta:
        model = Influencer
        depth = 1
        fields = (
            "id",
            "name",
            "gender",
            "category",
            "phone",
            "email",
            "bank",
            "IBAN",
            "account_holder_name",
            "accounts",
            "city",
            "branch",
        )


class CreateSocialAccountSerializer(ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ("id", "username", "platform", "influencer", "cost")


class SocialAccountSerializer(ModelSerializer):
    class Meta:
        model = SocialAccount
        depth = 1
        fields = ("id", "username", "platform", "influencer", "cost")
