import uuid
from django.db import models

from accounts.models import Organization, User
from core.constants import LeadStatus
from core.managers import OrganizationManager
from core.models import SoftDeleteBaseModel, SaaSBaseModel


class BusinessType(SaaSBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'business_types'
        unique_together = ['name', 'organization']


class LeadSource(SaaSBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'lead_sources'
        unique_together = ['name', 'organization']


class Lead(SaaSBaseModel, SoftDeleteBaseModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    source = models.ForeignKey(
        LeadSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=LeadStatus.CHOICES,
        default=LeadStatus.NEW,
        db_index=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_index=True,
        blank=True,
        null=True
    )

    estimated_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    priority_score = models.IntegerField(default=0)

    notes = models.TextField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    google_maps_url = models.URLField(blank=True, null=True)

    class Meta:
        default_related_name = 'leads'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'assigned_to']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['organization', 'status', 'created_at']),
            models.Index(fields=['organization', 'assigned_to', 'status']),
            models.Index(fields=['organization', 'status', 'assigned_to'])
        ]

    def __str__(self):
        return self.name



