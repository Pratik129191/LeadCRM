from core.constants import LeadStatus


STATUS_RANK = {
    LeadStatus.NEW: 1,
    LeadStatus.CALLED: 2,
    LeadStatus.FOLLOW_UP: 3,
    LeadStatus.INTERESTED: 4,
    LeadStatus.PROPOSAL_SENT: 5,
    LeadStatus.WON: 6,
    LeadStatus.LOST: 7,
}


def update_lead_status_from_activity(activity):
    if not activity.activity_type:
        return

    if not activity.activity_type.affects_pipeline:
        return

    new_status = activity.activity_type.pipeline_status

    if not new_status:
        return

    lead = activity.lead

    # Prevent status change if lead is already closed
    if lead.status in [LeadStatus.WON, LeadStatus.LOST]:
        return

    # LOST should always override if lead is still open
    if new_status == LeadStatus.LOST:
        lead.status = LeadStatus.LOST
        lead.save(update_fields=["status"])
        return

    current_rank = STATUS_RANK.get(lead.status, 0)
    new_rank = STATUS_RANK.get(new_status, 0)

    if new_rank > current_rank:
        lead.status = new_status
        lead.save(update_fields=["status"])


