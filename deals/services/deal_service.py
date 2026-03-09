from django.utils import timezone
from django.db import transaction

from deals.models import Deal, DealStage
from leads.models import Lead
from core.constants import LeadStatus


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

    lead.status = LeadStatus.INTERESTED
    lead.save(update_fields=["status"])

    return deal


def move_deal_stage(deal, stage):

    if deal.stage.is_closed:
        raise ValueError("Closed deal cannot move")

    if stage.organization != deal.organization:
        raise ValueError("Invalid stage")

    deal.stage = stage
    deal.save(update_fields=["stage"])


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


def reopen_deal(deal):

    if not deal.stage.is_closed:
        return

    stage = get_first_stage(deal.organization)

    deal.stage = stage
    deal.closed_at = None
    deal.closed_by = None

    deal.save(update_fields=["stage", "closed_at", "closed_by"])