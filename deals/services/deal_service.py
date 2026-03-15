from django.utils import timezone
from django.db import transaction

from deals.models import Deal, DealStage

from core.constants import LeadStatus, AuditAction, AuditEntity
from core.events.events import EventTypes
from core.events.event_bus import emit


class DealService:

    @staticmethod
    def get_first_stage(organization):
        return DealStage.objects.filter(
            organization=organization
        ).order_by("order").first()


    @staticmethod
    @transaction.atomic
    def convert_lead(lead, user):
        if lead.organization != user.organization:
            raise ValueError("Cross organization access")

        if hasattr(lead, "deal"):
            return lead.deal

        stage = DealService.get_first_stage(lead.organization)

        deal = Deal.objects.create(
            organization=lead.organization,
            lead=lead,
            stage=stage,
            value=lead.estimated_value or 0,
        )

        emit(
            event_type=EventTypes.DEAL_CREATED,
            payload={
                "organization": lead.organization,
                "user": user,
                "lead": lead,
                "action": AuditAction.DEAL_CREATED,
                "entity_type": AuditEntity.DEAL,
                "entity_id": deal.id,
                "metadata": {
                    "lead_id": str(lead.id),
                    "stage": stage.name
                }
            }
        )

        lead.status = LeadStatus.INTERESTED
        lead.save(update_fields=["status"])

        return deal


    @staticmethod
    def move_stage(deal, stage, user=None):
        if user and user.organization != deal.organization:
            raise ValueError("Cross organization access")

        if deal.stage.is_closed:
            raise ValueError("Closed deal cannot move")

        if stage.organization != deal.organization:
            raise ValueError("Invalid stage")

        deal.stage = stage
        deal.save(update_fields=["stage"])

        emit(
            event_type=EventTypes.DEAL_STAGE_CHANGED,
            payload={
                "organization": deal.organization,
                "user": user,
                "action": AuditAction.DEAL_STAGE_CHANGED,
                "lead": deal.lead,
                "entity_type": AuditEntity.DEAL,
                "entity_id": deal.id,
                "metadata": {
                    "new_stage": stage.name
                }
            }
        )


    @staticmethod
    def close_won(deal, user):
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

        emit(
            event_type=EventTypes.DEAL_WON,
            payload={
                "organization": deal.organization,
                "user": user,
                "action": AuditAction.DEAL_WON,
                "lead": deal.lead,
                "entity_type": AuditEntity.DEAL,
                "entity_id": deal.id
            }
        )


    @staticmethod
    def close_lost(deal, user):
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

        emit(
            event_type=EventTypes.DEAL_LOST,
            payload={
                "organization": deal.organization,
                "user": user,
                "action": AuditAction.DEAL_LOST,
                "lead": deal.lead,
                "entity_type": AuditEntity.DEAL,
                "entity_id": deal.id
            }
        )


    @staticmethod
    def reopen(deal, user=None):
        if not deal.stage.is_closed:
            return

        stage = DealService.get_first_stage(deal.organization)

        deal.stage = stage
        deal.closed_at = None
        deal.closed_by = None

        deal.save(update_fields=["stage", "closed_at", "closed_by"])

        emit(
            event_type=EventTypes.DEAL_REOPENED,
            payload={
                "organization": deal.organization,
                "user": user,
                "action": AuditAction.DEAL_REOPENED,
                "lead": deal.lead,
                "entity_type": AuditEntity.DEAL,
                "entity_id": deal.id,
            }
        )

