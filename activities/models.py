import uuid
from django.db import models

from accounts.models import Organization
from leads.models import Lead
from accounts.models import User
from core.constants import LeadStatus
from core.models import SoftDeleteBaseModel, SaaSBaseModel
from core.managers import OrganizationManager


class ActivityType(SaaSBaseModel):
    name = models.CharField(max_length=50)

    affects_pipeline = models.BooleanField(default=False)

    pipeline_status = models.CharField(
        max_length=30,
        choices=LeadStatus.CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        default_related_name = 'activity_types'
        unique_together = ['name', 'organization']

        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=["organization", "pipeline_status"])
        ]

    def __str__(self):
        return self.name


class Activity(SaaSBaseModel, SoftDeleteBaseModel):
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

    class Meta:
        default_related_name = 'activities'
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['lead']),
            models.Index(fields=['next_follow_up']),
        ]


    def save(self, *args, **kwargs):
        if self.lead and self.organization != self.lead.organization:
            raise ValueError("Lead Organization Mismatch.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity_type} - {self.lead}"

