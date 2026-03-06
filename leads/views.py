from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from activities.models import Activity
from accounts.models import User
from activities.forms import ActivityForm
from core.constants import LeadStatus
from .forms import LeadForm
from .models import Lead
from leads.services.pipeline_service import update_lead_status_from_activity


@login_required()
def lead_list(request):
    query = request.GET.get('q')

    if request.user.role == User.Role.SALES:
        leads = Lead.objects.filter(
            organization=request.user.organization,
            is_deleted=False,
        ).filter(
            Q(assigned_to=request.user) | Q(assigned_to__isnull=True)
        )
    else:
        leads = Lead.objects.filter(
            organization=request.user.organization,
            is_deleted=False,
        )

    # for search filed
    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    leads = leads.order_by('-created_at').select_related('assigned_to', 'business_type')

    paginator = Paginator(leads, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'leads': page_obj,
        'query': query,
        'page_obj': page_obj
    }

    return render(
        request,
        'leads/lead_list.html',
        context
    )


@login_required()
def lead_detail(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
        is_deleted=False,
        organization=request.user.organization
    )

    # Sales users can only access their leads
    if request.user.role == User.Role.SALES and lead.assigned_to != request.user:
        return redirect("lead_list")

    activities = lead.activities.filter(
        is_deleted=False
    ).select_related('user', 'activity_type').order_by('-created_at')

    form = ActivityForm(user=request.user)

    if request.method == 'POST':
        form = ActivityForm(request.POST, user=request.user)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.lead = lead
            activity.user = request.user
            activity.organization = request.user.organization

            if activity.activity_type.organization != request.user.organization:
                return redirect("lead_detail", pk=lead.pk)
            activity.save()

            update_lead_status_from_activity(activity)
            return redirect('lead_detail', pk=lead.pk)

    context = {
        'lead': lead,
        'activities': activities,
        'form': form,
    }

    return render(
        request,
        'leads/lead_detail.html',
        context
    )


@login_required()
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST, user=request.user)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.organization = request.user.organization

            if request.user.role == User.Role.SALES:
                lead.assigned_to = request.user

            lead.save()
            return redirect('lead_list')
    else:
        form = LeadForm(user=request.user)

    return render(
        request,
        'leads/lead_create.html',
        {'form': form}
    )


@login_required()
def lead_update(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
        is_deleted=False,
        organization=request.user.organization
    )

    if request.user.role == User.Role.SALES and lead.assigned_to != request.user:
        return redirect("lead_list")

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('lead_detail', pk=pk)
    else:
        form = LeadForm(instance=lead, user=request.user)

    return render(
        request,
        'leads/lead_create.html',
        {'form': form}
    )


@login_required()
def pipeline(request):
    base_query = Lead.objects.filter(
        organization=request.user.organization,
        is_deleted=False
    ).select_related(
        'assigned_to',
        'business_type'
    )

    if request.user.role == User.Role.SALES:
        base_query = base_query.filter(assigned_to=request.user)

    context = {
        "new_leads": base_query.filter(
            status=LeadStatus.NEW
        ),

        "called_leads": base_query.filter(
            status=LeadStatus.CALLED
        ),

        "followup_leads": base_query.filter(
            status=LeadStatus.FOLLOW_UP
        ),

        "interested_leads": base_query.filter(
            status=LeadStatus.INTERESTED
        ),

        "proposal_leads": base_query.filter(
            status=LeadStatus.PROPOSAL_SENT
        ),

        "won_leads": base_query.filter(
            status=LeadStatus.WON
        ),

        "lost_leads": base_query.filter(
            status=LeadStatus.LOST
        ),
    }

    return render(
        request,
        'leads/pipeline.html',
        context
    )


