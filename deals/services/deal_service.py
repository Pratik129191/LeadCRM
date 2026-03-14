from django.utils import timezone
from django.db import transaction

from deals.models import Deal, DealStage
from core.services.audit_service import log_event
from core.constants import LeadStatus, AuditAction, AuditEntity


def get_first_stage(organization):
    return DealStage.objects.filter(
        organization=organization
    ).order_by("order").first()


@transaction.atomic
def convert_lead_to_deal(lead, user):

    if lead.organization != user.organization:
        raise ValueError("Cross organization access")

    if hasattr(lead, "deal"):
        return lead.deal

    stage = get_first_stage(lead.organization)

    deal = Deal.objects.create(
        organization=lead.organization,
        lead=lead,
        stage=stage,
        value=lead.estimated_value or 0,
    )

    log_event(
        organization=lead.organization,
        user=user,
        action=AuditAction.DEAL_CREATED,
        entity_type=AuditEntity.DEAL,
        entity_id=deal.id,
        metadata={
            "lead_id": str(lead.id),
            "stage": stage.name
        }
    )

    lead.status = LeadStatus.INTERESTED
    lead.save(update_fields=["status"])

    return deal


def move_deal_stage(deal, stage, user=None):

    if deal.stage.is_closed:
        raise ValueError("Closed deal cannot move")

    if stage.organization != deal.organization:
        raise ValueError("Invalid stage")

    deal.stage = stage
    deal.save(update_fields=["stage"])

    log_event(
        organization=deal.organization,
        user=user,
        action=AuditAction.DEAL_STAGE_CHANGED,
        entity_type=AuditEntity.DEAL,
        entity_id=deal.id,
        metadata={
            "new_stage": stage.name,
        }
    )


def close_deal_won(deal, user):

    stage = DealStage.objects.filter(
        organization=deal.organization,
        is_closed=True,
        is_won=True
    ).first()

    if not stage:
        raise ValueError("Won stage not configured")

    deal.stage = stage
    deal.closed_by = user
    deal.closed_at = timezone.now()

    deal.save(update_fields=["stage", "closed_by", "closed_at"])

    log_event(
        organization=deal.organization,
        user=user,
        action=AuditAction.DEAL_WON,
        entity_type=AuditEntity.DEAL,
        entity_id=deal.id
    )


def close_deal_lost(deal, user):

    stage = DealStage.objects.filter(
        organization=deal.organization,
        is_closed=True,
        is_won=False
    ).first()

    if not stage:
        raise ValueError("Lost stage not configured")

    deal.stage = stage
    deal.closed_by = user
    deal.closed_at = timezone.now()

    deal.save(update_fields=["stage", "closed_by", "closed_at"])

    log_event(
        organization=deal.organization,
        user=user,
        action=AuditAction.DEAL_LOST,
        entity_type=AuditEntity.DEAL,
        entity_id=deal.id
    )


def reopen_deal(deal, user=None):

    if not deal.stage.is_closed:
        return

    stage = get_first_stage(deal.organization)

    deal.stage = stage
    deal.closed_at = None
    deal.closed_by = None

    deal.save(update_fields=["stage", "closed_at", "closed_by"])

    log_event(
        organization=deal.organization,
        user=user,
        action=AuditAction.DEAL_REOPENED,
        entity_type=AuditEntity.DEAL,
        entity_id=deal.id
    )