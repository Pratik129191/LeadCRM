from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from activities.models import Activity
from deals.models import Deal
from leads.models import Lead


class LeadScoringService:
    VIP_THRESHOLD = 80

    @staticmethod
    def compute_score(lead: Lead):
        score = 0

        # ---------------- Estimated Value Weight ----------------
        if lead.estimated_value:
            if lead.estimated_value > 200000:
                score += 40
            elif lead.estimated_value > 50000:
                score += 25
            elif lead.estimated_value > 10000:
                score += 10

        # ---------------- Activity Engagement ----------------
        activity_count = Activity.objects.filter(lead=lead).count()
        score += min(activity_count * 5, 25)

        # ---------------- Recent Engagement Bonus ----------------
        recent_threshold = timezone.now() - timedelta(days=7)
        recent_activity = Activity.objects.filter(
            lead=lead,
            created_at__gte=recent_threshold,
        ).exists()

        if recent_activity:
            score += 10

        # ---------------- Deal Stage Weight ----------------
        if hasattr(lead, 'deal'):
            deal = lead.deal

            if deal.stage.is_won:
                score += 30
            elif not deal.stage.is_closed:
                score += 15

        return score


    @staticmethod
    def update_lead_score(lead: Lead):
        score = LeadScoringService.compute_score(lead)
        lead.priority_score = score

        if score >= LeadScoringService.VIP_THRESHOLD:
            lead.is_vip = True
        else:
            lead.is_vip = False

        lead.save(update_fields=['priority_score', 'is_vip'])




