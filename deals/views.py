from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import DealStage, Deal
from leads.models import Lead
from deals.services.deal_service import (
    convert_lead_to_deal,
    move_deal_stage,
    close_deal_won,
    close_deal_lost,
    reopen_deal
)


@login_required
def deal_pipeline(request):

    org = request.organization

    stages = DealStage.objects.filter(
        organization=org
    ).order_by("order")

    deals = Deal.objects.for_org(request.organization).select_related(
        "lead",
        "stage"
    )

    stage_map = {stage.id: [] for stage in stages}

    for deal in deals:
        stage_map[deal.stage_id].append(deal)

    context = {
        "stages": stages,
        "stage_map": stage_map
    }

    return render(
        request,
        "deals/pipeline.html",
        context
    )


@login_required
def convert_lead(request, lead_id):
    lead = get_object_or_404(
        Lead.objects.for_org(request.organization).active(),
        id=lead_id
    )

    deal = convert_lead_to_deal(lead, request.user)
    return redirect('deal_detail', deal.id)


@login_required
def deal_detail(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.for_org(request.organization).select_related("lead", "stage"),
        id=deal_id
    )

    stages = DealStage.objects.filter(
        organization=request.organization
    ).order_by("order")

    context = {
        "deal": deal,
        "stages": stages
    }

    return render(
        request,
        "deals/deal_detail.html",
        context
    )


@login_required
def move_deal_stage_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.for_org(request.organization),
        id=deal_id
    )

    stage_id = request.POST.get("stage_id")

    stage = get_object_or_404(
        DealStage,
        id=stage_id,
        organization=request.organization
    )

    move_deal_stage(deal, stage, user=request.user)

    return redirect("deal_detail", deal_id=deal.id)


@login_required
def close_deal_won_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.for_org(request.organization),
        id=deal_id
    )
    close_deal_won(deal, request.user)
    return redirect("deal_detail", deal_id=deal.id)


@login_required
def close_deal_lost_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.for_org(request.organization),
        id=deal_id
    )
    close_deal_lost(deal, request.user)
    return redirect("deal_detail", deal_id=deal.id)


@login_required
def reopen_deal_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.for_org(request.organization),
        id=deal_id
    )
    reopen_deal(deal, user=request.user)
    return redirect("deal_detail", deal_id=deal.id)