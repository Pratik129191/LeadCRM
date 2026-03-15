import uuid
from django.db import models
from django.utils import timezone
from core.managers import OrganizationManager


class SaaSBaseModel(models.Model):
    objects = OrganizationManager()

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteBaseModel(models.Model):
    is_deleted = models.BooleanField(
        default=False,
        db_index=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class AuditLog(SaaSBaseModel):
    class AuditEntity(models.TextChoices):
        ACTIVITY = "ACTIVITY", "Activity"
        LEAD = "LEAD", "Lead"
        DEAL = "DEAL", "Deal"
        USER = "USER", "User"

    lead = models.ForeignKey(
        "leads.Lead",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )

    action = models.CharField(
        max_length=100,
        db_index=True
    )

    entity_type = models.CharField(
        max_length=50,
        choices=AuditEntity.choices,
        db_index=True
    )

    entity_id = models.UUIDField(
        db_index=True
    )

    metadata = models.JSONField(
        blank=True,
        null=True,
    )

    class Meta:
        default_related_name = "audit_logs"
        indexes = [
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return f"{self.entity_type}: {self.action}"



