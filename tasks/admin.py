from django.contrib import admin
from .models import Task, Reminder


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'assigned_to',
        'priority',
        'status',
        'due_date',
        'created_at',
    )

    list_filter = (
        'priority',
    )

    search_fields = (
        'title',
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'trigger_at',
        'sent'
    )













