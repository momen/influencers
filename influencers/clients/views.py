from datetime import date, timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import (
    ClientSerializer,
    CampaignSerializer,
    OfferSerializer,
    CreateClientSerializer,
    CreateOfferSerializer,
    CreateCampaignSerializer,
    AssignedInfluencerSerializer,
    CreateAssignedInfluencerSerializer,
    CalendarSerializer,
    InfluencerHistorySerializer,
    CreateInfluencerHistorySerializer,
    UpdateInfluencerHistorySerializer,
    InfluencerPaymentSerializer,
    InfluencerUnPaidNotificationSerializer,
    CreateInfluencerUnPaidNotificationSerializer,
)
from .models import (
    Client,
    Offer,
    Campaign,
    AssignedInfluencer,
    InfluencerHistory,
    InfluencerPayment,
    InfluencerUnPaidNotification,
)
from influencers.core.models import Coupon
from influencers.taskapp.helpers import get_days_range_from_today


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request:
            user = self.request.user
            if user.is_superuser or user.is_staff:
                return queryset
            else:
                return queryset.filter(account_manager=user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateClientSerializer
        return ClientSerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request:
            user = self.request.user
            if user.is_superuser or user.is_staff:
                return queryset
            else:
                return queryset.filter(client__account_manager=user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateOfferSerializer
        return OfferSerializer


class ClientOffersView(ListAPIView):

    """
    Retrieve a list of a client's offers
    """

    serializer_class = OfferSerializer
    queryset = Offer.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        client_id = self.kwargs.get("id")
        if self.request:
            user = self.request.user
            if not user.is_superuser or not user.is_staff:
                queryset = queryset.filter(client__account_manager=user)
        if client_id and isinstance(client_id, int):
            return queryset.filter(client__id=client_id)
        return queryset.none()


class CampaignViewSet(ModelViewSet):

    queryset = Campaign.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request:
            user = self.request.user
            if user.is_superuser or user.is_staff:
                return queryset
            else:
                return queryset.filter(account_manager=user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateCampaignSerializer
        return CampaignSerializer


class AssignedInfluencerList(ListCreateAPIView):
    """
    Get List of influencers assigned to a campaign or
    create record in AssignedInfluencer table to assign influencer to a campaign
    """

    queryset = AssignedInfluencer.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        campaign_id = self.kwargs.get("id")
        if campaign_id and isinstance(campaign_id, int):
            return queryset.filter(campaign__id=campaign_id)
        return queryset.none()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method == "POST":
            return CreateAssignedInfluencerSerializer
        return AssignedInfluencerSerializer

    def perform_create(self, serializer):
        coupon = Coupon.objects.create()
        coupon.percentage = serializer.validated_data["discount"]
        coupon.save()
        serializer.save(coupon=coupon)


class AssignedInfluencerDetail(RetrieveUpdateDestroyAPIView):
    """
    Edit assigned influencer to a campaign or
    Delete influencer assigned from a campaign
    """

    queryset = AssignedInfluencer.objects.all()
    lookup_field = "id"

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method == "PUT":
            return CreateAssignedInfluencerSerializer
        return AssignedInfluencerSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        coupon = instance.coupon
        coupon.percentage = serializer.validated_data["discount"]
        coupon.save()
        serializer.save(coupon=coupon)


class InfluencerHistoryList(ListCreateAPIView):
    """
    Get List of sales assigned to campaign assigned influencer
    create record in InfluencerHistory table to assign sales
    """

    queryset = InfluencerHistory.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset
        assigned_id = self.kwargs.get("id")
        if assigned_id and isinstance(assigned_id, int):
            return queryset.filter(assigned_influencer__id=assigned_id)
        return queryset.none()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method == "POST":
            return CreateInfluencerHistorySerializer
        return InfluencerHistorySerializer


class InfluencerHistoryDetail(RetrieveUpdateDestroyAPIView):
    """
    Edit assigned influencer history or
    Delete assigned influencer history
    """

    queryset = InfluencerHistory.objects.all()
    serializer_class = UpdateInfluencerHistorySerializer
    lookup_field = "id"


class CalendarViewSet(ModelViewSet):
    queryset = AssignedInfluencer.objects.all()
    serializer_class = CalendarSerializer


class InfluencerPaymentViewSet(ModelViewSet):
    queryset = InfluencerPayment.objects.all()
    serializer_class = InfluencerPaymentSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.assigned_influencer = self.request.data.get("assigned_influencer")
        serializer.invoice = self.request.FILES.get("file")
        serializer.billing_status = "PAID"
        serializer.day = self.request.data.get("day")
        serializer.save()

    def perform_destroy(self, instance):
        instance.billing_status = "UNPAID"
        instance.save()


class InfluencerUnPaidNotificationViewSet(ModelViewSet):
    queryset = InfluencerUnPaidNotification.objects.all()

    def get_queryset(self, *args, **kwargs):
        days_before, days_after = get_days_range_from_today()
        unpaid_lst_notify = InfluencerUnPaidNotification.objects.filter(
            day__range=[days_before, days_after]
        ).all()
        if unpaid_lst_notify:
            return unpaid_lst_notify
        else:
            return self.queryset.none()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method == "POST":
            return CreateInfluencerUnPaidNotificationSerializer
        return InfluencerUnPaidNotificationSerializer
