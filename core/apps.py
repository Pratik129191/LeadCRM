from django.apps import AppConfig



class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):

        # --------------- importing here to avoid AppRegistryNotReady ---------------
        from .events.event_bus import register
        from .events.listeners import audit_listener
        from .events.events import EventTypes
        from leads.services.scoring_listener import lead_scoring_listener
        from notifications.services.notification_service import create_notification

        # --------------- Audit Log Listeners ---------------
        register(EventTypes.LEAD_CREATED, audit_listener)
        register(EventTypes.ACTIVITY_CREATED, audit_listener)
        register(EventTypes.DEAL_CREATED, audit_listener)
        register(EventTypes.DEAL_REOPENED, audit_listener)
        register(EventTypes.DEAL_STAGE_CHANGED, audit_listener)
        register(EventTypes.DEAL_LOST, audit_listener)
        register(EventTypes.NOTE_CREATED, audit_listener)
        register(EventTypes.TASK_CREATED, audit_listener)
        register(EventTypes.TASK_COMPLETED, audit_listener)

        # --------------- Lead Scoring Listeners ---------------
        register(EventTypes.ACTIVITY_CREATED, lead_scoring_listener)
        register(EventTypes.DEAL_CREATED, lead_scoring_listener)
        register(EventTypes.DEAL_REOPENED, lead_scoring_listener)

        # --------------- Notification Service Listeners ---------------
        register(EventTypes.REMINDER_TRIGGERED, create_notification)


