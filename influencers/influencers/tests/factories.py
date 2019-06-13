from factory import DjangoModelFactory
from influencers.influencers.models import Influencer, SocialAccount


class InfluencerFactory(DjangoModelFactory):
    class Meta:
        model = Influencer


class SocialAccountFactory(DjangoModelFactory):
    class Meta:
        model = SocialAccount
