from django.contrib import admin
from .models import Category, SocialPlatform, Bank, Coupon


class BankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "swift")


class CouponAdmin(admin.ModelAdmin):
    fields = ("percentage",)


admin.site.register(Category)
admin.site.register(SocialPlatform)
admin.site.register(Bank, BankAdmin)
admin.site.register(Coupon, CouponAdmin)
