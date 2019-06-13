from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, SocialPlatformSerializer, BankSerializer
from .models import Category, SocialPlatform, Bank


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SocialPlatformViewSet(ModelViewSet):
    serializer_class = SocialPlatformSerializer
    queryset = SocialPlatform.objects.all()


class BankViewSet(ModelViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
