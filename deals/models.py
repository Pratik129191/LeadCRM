import uuid
from django.db import models

from accounts.models import Organization, User
from core.managers import OrganizationManager
from core.models import SaaSBaseModel
from leads.models import Lead


class DealStage(SaaSBaseModel):
    name = models.CharField(
        max_length=100
    )

    order = models.PositiveIntegerField(
        help_text="Pipeline order"
    )

    is_closed = models.BooleanField(
        default=False,
        help_text="Stage closes the deal"
    )

    is_won = models.BooleanField(
        default=False,
        help_text="Marks deal as won"
    )

    class Meta:
        default_related_name = 'deal_stages'
        ordering = ["order"]
        unique_together = ["organization", "name"]
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["organization", "order"]),
        ]

    def __str__(self):
        return self.name


class Deal(SaaSBaseModel):
    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name="deal"
    )

    stage = models.ForeignKey(
        DealStage,
        on_delete=models.PROTECT,
        related_name="deals",
        db_index=True
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_index=True
    )

    closed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'deals'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['organization', 'stage']),
            models.Index(fields=['organization', 'closed_at']),
            models.Index(fields=['organization', 'value']),
        ]

    def is_closed(self):
        return self.stage.is_closed

    def __str__(self):
        return f"Deal - {self.lead}"


