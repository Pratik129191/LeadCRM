from django.apps import AppConfig

from leads.services.scoring_listener import lead_scoring_listener

from .events.event_bus import register
from .events.listeners import audit_listener
from .events.events import EventTypes



class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # --------------- Audit Log Listeners ---------------
        register(EventTypes.LEAD_CREATED, audit_listener)
        register(EventTypes.ACTIVITY_CREATED, audit_listener)
        register(EventTypes.DEAL_CREATED, audit_listener)
        register(EventTypes.DEAL_REOPENED, audit_listener)
        register(EventTypes.DEAL_STAGE_CHANGED, audit_listener)
        register(EventTypes.DEAL_LOST, audit_listener)

        # --------------- Lead Scoring Listeners ---------------
        register(EventTypes.ACTIVITY_CREATED, lead_scoring_listener)
        register(EventTypes.DEAL_CREATED, lead_scoring_listener)
        register(EventTypes.DEAL_REOPENED, lead_scoring_listener)


