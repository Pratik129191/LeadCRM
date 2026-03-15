from django.db import models
from core.models import SaaSBaseModel
from accounts.models import User
from leads.models import Lead
from deals.models import Deal


class Task(SaaSBaseModel):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    title = models.CharField(max_length=120)

    description = models.TextField(
        blank=True,
        null=True,
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )


class Reminder(SaaSBaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='reminders',
    )

    trigger_at = models.DateTimeField()

    sent = models.BooleanField(default=False)












