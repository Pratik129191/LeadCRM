from django.core.management.base import BaseCommand
from django.utils import timezone

from tasks.models import Reminder
from core.events.event_bus import emit
from core.events.events import EventTypes
from core.tenant_context import set_system_mode, clear_system_mode


class Command(BaseCommand):
    help = "Process task reminders"

    def handle(self, *args, **options):
        set_system_mode()
        try:
            now = timezone.now()
            reminders = Reminder.objects.filter(
                trigger_at__lte=now,
                sent=False
            ).select_related('task')

            for reminder in reminders:
                emit(
                    event_type=EventTypes.REMINDER_TRIGGERED,
                    payload={
                        "organization": reminder.organization,
                        "task": reminder.task,
                        "user": reminder.task.assigned_to,
                    }
                )
                reminder.sent = True
                reminder.save(update_fields=["sent"])
        finally:
            clear_system_mode()




