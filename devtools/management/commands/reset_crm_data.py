from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Organization, User
from leads.models import Lead, BusinessType, LeadSource
from activities.models import Activity, ActivityType
from deals.models import Deal, DealStage
from core.models import AuditLog
from core.tenant_context import set_system_mode, clear_system_mode


class Command(BaseCommand):

    help = "Reset all CRM demo data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        set_system_mode()

        try:

            self.stdout.write("Deleting Audit Logs...")
            AuditLog.objects.all().delete()

            self.stdout.write("Deleting Activities...")
            Activity.objects.all().delete()

            self.stdout.write("Deleting Deals...")
            Deal.objects.all().delete()

            self.stdout.write("Deleting Deal Stages...")
            DealStage.objects.all().delete()

            self.stdout.write("Deleting Leads...")
            Lead.objects.all().delete()

            self.stdout.write("Deleting Activity Types...")
            ActivityType.objects.all().delete()

            self.stdout.write("Deleting Business Types...")
            BusinessType.objects.all().delete()

            self.stdout.write("Deleting Lead Sources...")
            LeadSource.objects.all().delete()

            self.stdout.write("Deleting Users...")
            User.objects.all().delete()

            self.stdout.write("Deleting Organizations...")
            Organization.objects.all().delete()

        finally:
            clear_system_mode()

        self.stdout.write(self.style.SUCCESS("CRM database reset complete"))




