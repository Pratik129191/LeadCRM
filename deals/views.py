from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import DealStage, Deal
from leads.models import Lead
from deals.services.deal_service import DealService


@login_required
def deal_pipeline(request):

    org = request.organization

    stages = DealStage.objects.filter(
        organization=org
    ).order_by("order")

    deals = Deal.objects.filter(
        organization=org
    ).select_related(
        "lead",
        "stage",
        "lead__assigned_to",
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
        Lead.objects.active(),
        id=lead_id
    )

    deal = DealService.convert_lead(lead, request.user)
    return redirect('deal_detail', deal.id)


@login_required
def deal_detail(request, deal_id):
    deal = get_object_or_404(
        Deal.objects.select_related("lead", "stage", "lead__assigned_to"),
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
        Deal.objects,
        id=deal_id
    )

    stage_id = request.POST.get("stage_id")

    stage = get_object_or_404(
        DealStage.objects.filter(organization=request.organization),
        id=stage_id
    )

    DealService.move_stage(deal, stage, user=request.user)

    return redirect("deal_detail", deal_id=deal.id)


@login_required
def close_deal_won_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects,
        id=deal_id
    )
    DealService.close_won(deal, request.user)
    return redirect("deal_detail", deal_id=deal.id)


@login_required
def close_deal_lost_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects,
        id=deal_id
    )
    DealService.close_lost(deal, request.user)
    return redirect("deal_detail", deal_id=deal.id)


@login_required
def reopen_deal_view(request, deal_id):
    deal = get_object_or_404(
        Deal.objects,
        id=deal_id
    )
    DealService.reopen(deal, user=request.user)
    return redirect("deal_detail", deal_id=deal.id)