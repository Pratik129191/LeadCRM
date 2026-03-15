from django.apps import AppConfig
from .events.event_bus import register
from .events.listeners import audit_listener
from .events.events import EventTypes


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        register(EventTypes.LEAD_CREATED, audit_listener)
        register(EventTypes.ACTIVITY_CREATED, audit_listener)
        register(EventTypes.DEAL_CREATED, audit_listener)
        register(EventTypes.DEAL_REOPENED, audit_listener)
        register(EventTypes.DEAL_STAGE_CHANGED, audit_listener)
        register(EventTypes.DEAL_LOST, audit_listener)


