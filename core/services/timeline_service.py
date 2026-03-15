from itertools import chain
from operator import attrgetter

from activities.models import Activity
from leads.models import Lead
from core.models import AuditLog
from core.constants import EntityType
from notes.models import Note


def get_lead_timeline(lead: Lead):
    """
    Returns a unified timeline for a given lead.
    combines activities and audit logs.
    :param lead:
    :return: list of activities for single lead
    """

    activities = Activity.objects.active().filter(
        lead=lead
    ).select_related(
        'user', 'activity_type'
    )

    audit_logs = AuditLog.objects.select_related("user").filter(
        organization=lead.organization,
        lead=lead,
    )

    notes = Note.objects.filter(
        lead=lead,
    ).select_related("user")

    timeline = list(chain(activities, audit_logs, notes))
    timeline.sort(key=attrgetter('created_at'), reverse=True)

    return timeline






