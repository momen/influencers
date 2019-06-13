from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from djoser.views import UserCreateView, PasswordResetView, PasswordResetConfirmView
from .views import (
    ListPermissions,
    CheckPermissions,
    ListActions,
    GroupViewSet,
    UserViewSet,
    LoginView,
)

app_name = "users"

router = DefaultRouter()
router.register(r"groups", GroupViewSet)
router.register(r"", UserViewSet)

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("register/", UserCreateView.as_view()),
    path("reset_password/", PasswordResetView.as_view()),
    path("reset_confirm/", PasswordResetConfirmView.as_view()),
    path("permissions/check/", CheckPermissions.as_view()),
    path("permissions/", ListPermissions.as_view()),
    path("actions/", ListActions.as_view()),
] + router.urls
