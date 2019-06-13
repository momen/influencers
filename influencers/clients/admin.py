from django.contrib import admin
from .models import (
    Client,
    Offer,
    Campaign,
    AssignedInfluencer,
    InfluencerHistory,
    InfluencerPayment,
    InfluencerUnPaidNotification,
)


admin.site.register(Client)
admin.site.register(Offer)
admin.site.register(Campaign)
admin.site.register(AssignedInfluencer)
admin.site.register(InfluencerHistory)
admin.site.register(InfluencerPayment)
admin.site.register(InfluencerUnPaidNotification)
