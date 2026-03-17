from core.constants import EntityType
from ..models import Notification


def create_notification(event):
    task = event.get('task')
    user = event.get('user')

    Notification.objects.create(
        organization=task.organization,
        user=user,
        title="Task Reminder",
        message=f"Task '{task.title}' is due soon.",
        entity_type=EntityType.TASK,
        entity_id=task.id,
    )

