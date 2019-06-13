from auditlog.models import LogEntry
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SlugRelatedField,
    ReadOnlyField,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "password",
            "email",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = [
            "name",
            "email",
            "groups",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "user_permissions",
        ]


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainSerializer, cls).get_token(user)
        token["name"] = user.name
        token["superuser"] = user.is_superuser
        token["staff"] = user.is_staff
        token["id"] = user.id
        return token


class GroupSerializer(ModelSerializer):
    user_set = PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(ModelSerializer):
    content_type = SlugRelatedField(
        slug_field="app_label", queryset=ContentType.objects.all()
    )

    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type"]


class LogEntrySerializer(ModelSerializer):
    action_type = ReadOnlyField(source="get_action_display")
    model = ReadOnlyField(source="content_type.model")
    changes = ReadOnlyField(source="changes_str")

    class Meta:
        model = LogEntry
        fields = ["timestamp", "actor", "action_type", "object_id", "model", "changes"]
