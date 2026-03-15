from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'entity_type',
        'created_at',
        'is_read'
    )

    list_filter = (
        'entity_type',
        'is_read'
    )








