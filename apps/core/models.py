import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(_("id"), default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    is_deleted = models.BooleanField(_("is_deleted"), default=False, editable=False)

    class Meta:
        abstract = True
