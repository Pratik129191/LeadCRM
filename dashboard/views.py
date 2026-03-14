from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from leads.models import Lead
from core.constants import LeadStatus
from activities.models import Activity
from deals.models import Deal
from datetime import date


@login_required()
def dashboard(request):
    org = request.organization
    today = date.today()

    total_leads = Lead.objects.select_related('assigned_to').for_org(org).active().count()

    interested_leads = Lead.objects.for_org(org).active().filter(
        status=LeadStatus.INTERESTED
    ).count()

    won_leads = Lead.objects.for_org(org).active().filter(
        status=LeadStatus.WON
    ).count()

    pipeline_value = Lead.objects.for_org(org).active().aggregate(
        total=Sum('estimated_value')
    )['total'] or 0

    followups_today = Activity.objects.for_org(org).active().filter(
        next_follow_up__date=today
    ).count()

    won_revenue = Deal.objects.for_org(org).filter(
        stage__is_won=True
    ).aggregate(total=Sum("value"))["total"] or 0

    open_pipeline_value = Deal.objects.for_org(org).filter(
        stage__is_closed=False
    ).aggregate(total=Sum("value"))["total"] or 0

    won_deals = Deal.objects.for_org(org).filter(
        stage__is_won=True
    ).count()

    lost_deals = Deal.objects.for_org(org).filter(
        stage__is_closed=True,
        stage__is_won=False
    ).count()

    context = {
        'total_leads': total_leads,
        'interested_leads': interested_leads,
        'won_leads': won_leads,
        'pipeline_value': pipeline_value,
        'followups_today': followups_today,
        "won_revenue": won_revenue,
        "open_pipeline_value": open_pipeline_value,
        "won_deals": won_deals,
        "lost_deals": lost_deals,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )



