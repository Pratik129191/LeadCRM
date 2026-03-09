from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import DealStage, Deal


@login_required
def deal_pipeline(request):

    org = request.user.organization

    stages = DealStage.objects.filter(
        organization=org
    ).order_by("order")

    deals = Deal.objects.filter(
        organization=org
    ).select_related(
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