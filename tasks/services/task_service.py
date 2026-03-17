from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from core.events.event_bus import emit
from core.events.events import EventTypes
from core.constants import EntityType, AuditAction
from tasks.services.reminder_service import ReminderService
from ..models import Task


class TaskService:

    @staticmethod
    @transaction.atomic
    def create_task(
            organization,
            title,
            assigned_to,
            user,
            lead=None,
            deal=None,
            due_date=None,
            priority=Task.Priority.MEDIUM
    ):
        task = Task.objects.create(
            organization=organization,
            title=title,
            assigned_to=assigned_to,
            lead=lead,
            deal=deal,
            due_date=due_date,
            priority=priority,
        )

        if due_date:
            reminder_time = due_date - timedelta(hours=2)
            ReminderService.create_reminder(
                task=task,
                trigger_at=reminder_time,
            )

        emit(
            event_type=EventTypes.TASK_CREATED,
            payload={
                "organization": organization,
                "user": user,
                "action": AuditAction.TASK_CREATED,
                "entity_type": EntityType.TASK,
                "entity_id": task.id,
                "lead": lead,
            },
        )

        return task





