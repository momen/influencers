from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from .models import Influencer, SocialAccount
from .serializers import (
    InfluencerSerializer,
    SocialAccountSerializer,
    CreateInfluencerSerializer,
    CreateSocialAccountSerializer,
)


class InfluencerViewSet(ModelViewSet):
    queryset = Influencer.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateInfluencerSerializer
        return InfluencerSerializer


class SocialAccountViewSet(ModelViewSet):
    queryset = SocialAccount.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateSocialAccountSerializer
        return SocialAccountSerializer


class InfluencerAccountsView(ListCreateAPIView):

    """
    Retrieve a list of an influencer's social accounts
    """

    serializer_class = SocialAccountSerializer
    queryset = SocialAccount.objects.all()

    def get_queryset(self, *args, **kwargs):
        influencer_id = self.kwargs.get("id")
        if influencer_id and isinstance(influencer_id, int):
            return self.queryset.filter(influencer__id=influencer_id)
        return self.queryset.none()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateSocialAccountSerializer
        return SocialAccountSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        if self.request and isinstance(self.request.data, list):
            kwargs["many"] = True
        return serializer_class(*args, **kwargs)
