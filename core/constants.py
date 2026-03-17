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

    NOTE_CREATED = "NOTE_CREATED"

    TASK_CREATED = "TASK_CREATED"
    TASK_COMPLETED = "TASK_COMPLETED"


class EntityType:
    LEAD = "LEAD"
    ACTIVITY = "ACTIVITY"
    DEAL = "DEAL"
    USER = "USER"
    TASK = "TASK"
    NOTE = "NOTE"

    CHOICES = [
        (LEAD, "Lead"),
        (ACTIVITY, "Activity"),
        (DEAL, "Deal"),
        (USER, "User"),
        (TASK, "Task"),
        (NOTE, "Note"),
    ]

