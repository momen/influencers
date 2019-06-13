from rest_framework.serializers import ModelSerializer, ValidationError
from django.db.utils import IntegrityError
from .models import Category, SocialPlatform, Bank


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        depth = 1
        fields = ("id", "name")


class SocialPlatformSerializer(ModelSerializer):
    class Meta:
        model = SocialPlatform
        depth = 1
        fields = ("id", "name")


class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        depth = 1
        fields = ("id", "name", "swift")

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            return instance
        except IntegrityError:
            raise ValidationError(
                {"swift": [u"Bank with this SWIFT code already exists."]}
            )
