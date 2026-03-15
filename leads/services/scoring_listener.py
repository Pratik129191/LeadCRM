from ..models import Lead
from ..services.scoring_service import LeadScoringService


def lead_scoring_listener(event):
    lead = event.get('lead')

    if not lead:
        return

    LeadScoringService().update_lead_score(lead)





