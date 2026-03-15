from django.db import models
from core.models import SaaSBaseModel
from accounts.models import User
from leads.models import Lead
from deals.models import Deal


class Note(SaaSBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="lead_notes",
        related_query_name="lead_note",
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="deal_notes",
        related_query_name="deal_note",
    )

    content = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['lead']),
            models.Index(fields=['deal']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Note by {self.user}"


class Attachment(SaaSBaseModel):
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    file = models.FileField(
        upload_to='crm_attachments/',
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="lead_attachments",
        related_query_name="lead_attachment",
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="deal_attachments",
        related_query_name="deal_attachment",
    )

    class Meta:
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['lead']),
            models.Index(fields=['deal']),
        ]






