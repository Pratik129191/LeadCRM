class LeadStatus:

    NEW = "NEW"
    CALLED = "CALLED"
    FOLLOW_UP = "FOLLOW_UP"
    INTERESTED = "INTERESTED"
    PROPOSAL_SENT = "PROPOSAL_SENT"
    WON = "WON"
    LOST = "LOST"

    CHOICES = [
        (NEW, "New"),
        (CALLED, "Called"),
        (FOLLOW_UP, "Follow Up"),
        (INTERESTED, "Interested"),
        (PROPOSAL_SENT, "Proposal Sent"),
        (WON, "Won"),
        (LOST, "Lost"),
    ]


class AuditAction:
    LEAD_CREATED = "LEAD_CREATED"
    LEAD_UPDATED = "LEAD_UPDATED"
    LEAD_DELETED = "LEAD_DELETED"

    ACTIVITY_CREATED = "ACTIVITY_CREATED"

    DEAL_CREATED = "DEAL_CREATED"
    DEAL_STAGE_CHANGED = "DEAL_STAGE_CHANGED"
    DEAL_WON = "DEAL_WON"
    DEAL_LOST = "DEAL_LOST"
    DEAL_REOPENED = "DEAL_REOPENED"


class AuditEntity:
    LEAD = "LEAD"
    ACTIVITY = "ACTIVITY"
    DEAL = "DEAL"
    USER = "USER"

