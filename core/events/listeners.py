from core.services.audit_service import log_event
from core.constants import EntityType


def audit_listener(event):
    log_event(
        organization=event.get('organization'),
        user=event.get('user'),
        action=event.get('action'),
        entity_type=event.get('entity_type'),
        entity_id=event.get('entity_id'),
        lead=event.get('lead'),
        metadata=event.get('metadata'),
    )




