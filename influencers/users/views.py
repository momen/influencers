from django.contrib.auth.models import Group, Permission
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from auditlog.models import LogEntry
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    GroupSerializer,
    PermissionSerializer,
    LogEntrySerializer,
    TokenObtainSerializer,
)
from .models import User


class UserViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request and self.request.method in ["POST", "PUT"]:
            return CreateUserSerializer
        return UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class ListPermissions(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class CheckPermissions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        permissions = request.data.get("permissions")
        if not permissions:
            raise ValidationError({"permissions": ["This field is required."]})
        if isinstance(permissions, list):
            user_permissions = {
                "permissions": [p for p in permissions if request.user.has_perm(p)]
            }
        elif isinstance(permissions, str):
            user_permissions = {
                "permissions": {permissions: request.user.has_perm(permissions)}
            }

        else:
            raise ValidationError(
                {"permissions": ["Please enter a valid permission name."]}
            )
        return Response(user_permissions)


class ListActions(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LogEntrySerializer
    queryset = LogEntry.objects.all()


class GroupViewSet(ModelViewSet):

    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = GroupSerializer
