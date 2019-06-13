from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField, EmailField, BooleanField, DateTimeField
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import Group
from auditlog.registry import auditlog
from partial_index import PartialIndex, PQ
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from influencers.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    _safedelete_policy = SOFT_DELETE_CASCADE
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_("email address"), blank=False, unique=True)
    is_staff = BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            PartialIndex(
                fields=["email", "deleted"], unique=True, where=PQ(deleted__isnull=True)
            )
        ]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


auditlog.register(User)
auditlog.register(Group)
