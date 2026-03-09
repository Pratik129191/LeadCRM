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
    org = request.user.organization
    today = date.today()

    total_leads = Lead.objects.select_related('assigned_to').filter(
        organization=org,
        is_deleted=False
    ).count()

    interested_leads = Lead.objects.filter(
        organization=org,
        is_deleted=False,
    status=LeadStatus.INTERESTED
    ).count()

    won_leads = Lead.objects.filter(
        organization=org,
        is_deleted=False,
        status=LeadStatus.WON
    ).count()

    pipeline_value = Lead.objects.filter(
        organization=org,
        is_deleted=False,
    ).aggregate(total=Sum('estimated_value'))['total'] or 0

    followups_today = Activity.objects.filter(
        organization=org,
        is_deleted=False,
        next_follow_up__date=today
    ).count()

    won_revenue = Deal.objects.filter(
        organization=org,
        stage__is_won=True
    ).aggregate(total=Sum("value"))["total"] or 0

    open_pipeline_value = Deal.objects.filter(
        organization=org,
        stage__is_closed=False
    ).aggregate(total=Sum("value"))["total"] or 0

    won_deals = Deal.objects.filter(
        organization=org,
        stage__is_won=True
    ).count()

    lost_deals = Deal.objects.filter(
        organization=org,
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



