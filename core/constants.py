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


class DealStatus:

    OPEN = "OPEN"
    WON = "WON"
    LOST = "LOST"

    CHOICES = [
        (OPEN, "Open"),
        (WON, "Won"),
        (LOST, "Lost"),
    ]