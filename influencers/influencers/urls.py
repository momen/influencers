from django.urls import path
from rest_framework.routers import DefaultRouter
from influencers.influencers.views import (
    InfluencerViewSet,
    SocialAccountViewSet,
    InfluencerAccountsView,
)


app_name = "influencers"

router = DefaultRouter()
router.register(r"socialaccount", SocialAccountViewSet)
router.register(r"", InfluencerViewSet)
urlpatterns = router.urls


# Append other urls of generic views(Not ViewSet)
urlpatterns += [
    path(
        "<int:id>/accounts/",
        InfluencerAccountsView.as_view(),
        name="influencer-accounts",
    )
]
