from core.models import AuditLog


def log_event(
        organization,
        user,
        action,
        entity_type,
        entity_id,
        metadata=None,
):
    AuditLog.objects.create(
        organization=organization,
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata or {},
    )

