from factory import DjangoModelFactory
from influencers.clients.models import (
    Client,
    Offer,
    Campaign,
    AssignedInfluencer,
    InfluencerHistory,
    InfluencerPayment,
)


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client


class OfferFactory(DjangoModelFactory):
    class Meta:
        model = Offer


class CampaignFactory(DjangoModelFactory):
    class Meta:
        model = Campaign


class AssignedInfluencerFactory(DjangoModelFactory):
    class Meta:
        model = AssignedInfluencer


class InfluencerHistoryFactory(DjangoModelFactory):
    class Meta:
        model = InfluencerHistory


class InfluencerPaymentFactory(DjangoModelFactory):
    class Meta:
        model = InfluencerPayment
