from django.db import models
from core.models import SaaSBaseModel
from core.constants import EntityType
from accounts.models import User


class Notification(SaaSBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    message = models.TextField()

    entity_type = models.CharField(
        max_length=50,
        choices=EntityType.CHOICES,
        db_index=True,
    )

    entity_id = models.UUIDField()

    is_read = models.BooleanField(default=False)






















