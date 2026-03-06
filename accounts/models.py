from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Organization(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=255)

    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='owned_organizations',
    )

    # SaaS ready fields
    subscription_plan = models.CharField(
        max_length=50,
        default="FREE"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
        ]

        unique_together = ['owner', 'name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        SALES = 'SALES', 'Sales Member'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SALES,
        db_index=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    is_active_member = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['role']),
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return f"{self.username} ({self.role})"


