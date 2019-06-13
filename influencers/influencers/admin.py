from django.contrib import admin
from .models import SocialAccount, Influencer


class InfluencerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "IBAN", "account_holder_name")


class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "influencer", "username", "platform")


admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(Influencer, InfluencerAdmin)
