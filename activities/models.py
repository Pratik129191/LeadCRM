import uuid
from django.db import models

from accounts.models import Organization
from leads.models import Lead
from accounts.models import User
from core.constants import LeadStatus


class ActivityType(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="activity_types"
    )

    name = models.CharField(max_length=50)

    affects_pipeline = models.BooleanField(default=False)

    pipeline_status = models.CharField(
        max_length=30,
        choices=LeadStatus.CHOICES,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'organization']

        indexes = [
            models.Index(fields=['organization']),
        ]

    def __str__(self):
        return self.name


class Activity(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='activities',
    )

    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.SET_NULL,
        null=True,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )

    note = models.TextField(blank=True, null=True)

    next_follow_up = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    is_completed = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['lead']),
            models.Index(fields=['next_follow_up']),
        ]

    def __str__(self):
        return f"{self.activity_type} - {self.lead}"

