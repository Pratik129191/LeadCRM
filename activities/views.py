from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
from .models import Activity
from accounts.models import User


@login_required()
def followups_today(request):
    today = date.today()
    activities = Activity.objects.for_org(
        request.organization
    ).active().filter(
        next_follow_up__date=today
    ).select_related('lead', 'user', 'activity_type')

    if request.user.role == User.Role.SALES:
        activities = activities.filter(user=request.user)

    return render(
        request,
        'activities/followups_today.html',
        {'activities': activities},
    )


@login_required()
def followups_overdue(request):
    today = date.today()
    activities = Activity.objects.for_org(
        request.organization
    ).active().filter(
        next_follow_up__date__lt=today
    ).select_related('lead', 'user', 'activity_type')

    if request.user.role == User.Role.SALES:
        activities = activities.filter(user=request.user)

    return render(
        request,
        'activities/followups_overdue.html',
        {'activities': activities},
    )



