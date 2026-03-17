from ..models import Reminder


class ReminderService:

    @staticmethod
    def create_reminder(task, trigger_at):
        return Reminder.objects.create(
            task=task,
            trigger_at=trigger_at,
            organization=task.organization,
        )




