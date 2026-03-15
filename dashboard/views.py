from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.core.cache import cache
from django.shortcuts import render

from leads.models import Lead

from core.constants import LeadStatus

from activities.models import Activity

from deals.models import Deal
from deals.services.forecast_service import ForecastService


@login_required()
def dashboard(request):
    org_id = str(request.organization.id)
    cache_key = f"org:{org_id}:dashboard"
    cached_data = cache.get(cache_key)

    if cached_data:
        return render(
            request,
            'dashboard/dashboard.html',
            cached_data
        )

    today = date.today()

    # -------- LEAD STATS (single query) --------
    lead_stats = Lead.objects.active().aggregate(
        total=Count("id"),
        interested=Count("id", filter=Q(status=LeadStatus.INTERESTED)),
        won=Count("id", filter=Q(status=LeadStatus.WON)),
        pipeline_value=Sum("estimated_value"),
    )

    # -------- FOLLOWUPS TODAY --------
    followups_today = Activity.objects.active().filter(
        next_follow_up__date=today
    ).count()

    # -------- DEAL STATS (single query) --------
    deal_stats = Deal.objects.filter(
        organization=request.organization
    ).aggregate(
        won_revenue=Sum("value", filter=Q(stage__is_won=True)),
        open_pipeline_value=Sum("value", filter=Q(stage__is_closed=False)),
        won_deals=Count("id", filter=Q(stage__is_won=True)),
        lost_deals=Count("id", filter=Q(stage__is_closed=True, stage__is_won=False)),
    )

    # -------- TOP LEADS --------
    top_leads = Lead.objects.active().order_by(
        "-priority_score"
    ).select_related(
        "assigned_to"
    )[:5]

    # -------- FORECAST PIPELINE --------
    expected_pipeline = ForecastService.pipeline_expected_revenue(request.organization)

    context = {
        "total_leads": lead_stats["total"] or 0,
        "interested_leads": lead_stats["interested"] or 0,
        "won_leads": lead_stats["won"] or 0,
        "pipeline_value": lead_stats["pipeline_value"] or 0,
        "followups_today": followups_today,
        "won_revenue": deal_stats["won_revenue"] or 0,
        "open_pipeline_value": deal_stats["open_pipeline_value"] or 0,
        "won_deals": deal_stats["won_deals"] or 0,
        "lost_deals": deal_stats["lost_deals"] or 0,
        "top_leads": top_leads,
        "expected_pipeline": expected_pipeline
    }

    cache.set(cache_key, context, 60)

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )

