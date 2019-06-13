from django.urls import path
from rest_framework.routers import DefaultRouter
from influencers.clients.views import (
    ClientViewSet,
    OfferViewSet,
    CampaignViewSet,
    CalendarViewSet,
    ClientOffersView,
    AssignedInfluencerList,
    AssignedInfluencerDetail,
    InfluencerHistoryList,
    InfluencerHistoryDetail,
    InfluencerPaymentViewSet,
    InfluencerUnPaidNotificationViewSet,
)


app_name = "clients"

router = DefaultRouter()
router.register(r"offers", OfferViewSet)
router.register(r"campaigns", CampaignViewSet)
router.register(r"", ClientViewSet)
router.register(r"calendar/history", CalendarViewSet)
router.register(r"influencers/unpaid", InfluencerUnPaidNotificationViewSet)
router.register(r"influencers/payment", InfluencerPaymentViewSet)
urlpatterns = router.urls


# Append other urls of generic views
urlpatterns += [
    path(r"<int:id>/offers/", ClientOffersView.as_view(), name="client-offers"),
    path(
        r"campaigns/<int:id>/influencers/",
        AssignedInfluencerList.as_view(),
        name="assign-influencers-list",
    ),
    path(
        r"campaigns/influencers/assign/<int:id>/",
        AssignedInfluencerDetail.as_view(),
        name="assign-influencers-detail",
    ),
    path(
        r"campaigns/influencers/assign/<int:id>/history/",
        InfluencerHistoryList.as_view(),
        name="influencer-history-list",
    ),
    path(
        r"campaigns/influencers/history/<int:id>/",
        InfluencerHistoryDetail.as_view(),
        name="influencer-history-detail",
    ),
]
