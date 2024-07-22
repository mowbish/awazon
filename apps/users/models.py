import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    is_suspended = models.BooleanField(default=False)
    gender = models.CharField(
        choices=[("MALE", _("MALE")), ("FEMALE", _("FEMALE"))],
        null=True,
        blank=True,
        max_length=220,
    )
    auth_level = models.SmallIntegerField(default=0)
    phone_number = models.CharField(max_length=11, unique=True)
    birthday = models.DateField(null=True, blank=True)
