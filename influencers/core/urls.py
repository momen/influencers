from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SocialPlatformViewSet, BankViewSet

app_name = "core"

router = DefaultRouter()
router.register(r"category", CategoryViewSet)
router.register(r"platform", SocialPlatformViewSet)
router.register(r"bank", BankViewSet)
urlpatterns = router.urls
