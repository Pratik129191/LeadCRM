import random
from decimal import Decimal
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User, Organization
from leads.models import Lead, BusinessType, LeadSource
from activities.models import Activity, ActivityType
from deals.models import DealStage, Deal

from core.constants import LeadStatus
from core.tenant_context import (
    set_current_organization,
    set_system_mode,
    clear_system_mode
)


FIRST_NAMES = [
    "Amit","Rahul","Priya","Neha","Rohit","Arjun","Sneha","Karan","Pooja",
    "Vikram","Ankit","Sanjay","Riya","Kavita","Raj","Aditya"
]

COMPANY_SUFFIX = [
    "Solutions","Technologies","Systems","Industries",
    "Enterprises","Digital","Consulting","Services","Group"
]

NOTES = [
    "Client interested in pricing",
    "Requested product demo",
    "Follow up next week",
    "Decision pending from management",
    "Budget discussion ongoing",
    "Requested proposal",
]


class Command(BaseCommand):

    help = "Generate realistic CRM dataset for testing"
    set_system_mode()

    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            # ---------------- ADMIN ----------------
            admin, created = User.objects.get_or_create(
                username="admin",
                defaults={
                    "role": User.Role.ADMIN,
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active_member": True
                }
            )

            if created:
                admin.set_password("Admin@123")
                admin.save()

            # ---------------- ORGANIZATION ----------------

            org, _ = Organization.objects.get_or_create(
                owner=admin,
                name="Demo CRM Organization"
            )

            set_current_organization(org)

            admin.organization = org
            admin.save(update_fields=["organization"])

            self.stdout.write("Admin + Organization ready")

            # ---------------- SALES TEAM ----------------

            sales_users = []

            for i in range(6):

                user, created = User.objects.get_or_create(
                    username=f"sales{i}",
                    defaults={
                        "role": User.Role.SALES,
                        "organization": org,
                        "is_active_member": True
                    }
                )

                if created:
                    user.set_password("Sales@123")
                    user.save()

                sales_users.append(user)

            self.stdout.write("Sales team ready")

            # ---------------- BUSINESS TYPES ----------------

            bt_names = [
                "Restaurant","Retail","Gym","Hospital",
                "Real Estate","School","Salon","Clinic"
            ]

            business_types = []

            for name in bt_names:
                obj, _ = BusinessType.objects.get_or_create(
                    name=name,
                    organization=org
                )
                business_types.append(obj)

            # ---------------- LEAD SOURCES ----------------

            source_names = [
                "Facebook Ads","Google Ads","Website",
                "Cold Call","Referral","LinkedIn"
            ]

            sources = []

            for name in source_names:
                obj, _ = LeadSource.objects.get_or_create(
                    name=name,
                    organization=org
                )
                sources.append(obj)

            # ---------------- ACTIVITY TYPES ----------------

            activity_types_data = [
                ("Call", True, LeadStatus.CALLED),
                ("Follow Up", True, LeadStatus.FOLLOW_UP),
                ("Interested", True, LeadStatus.INTERESTED),
                ("Proposal Sent", True, LeadStatus.PROPOSAL_SENT),
                ("Meeting", False, None),
                ("Note", False, None),
            ]

            activity_types = []

            for name, affects, status in activity_types_data:

                obj, _ = ActivityType.objects.get_or_create(
                    name=name,
                    organization=org,
                    defaults={
                        "affects_pipeline": affects,
                        "pipeline_status": status
                    }
                )

                activity_types.append(obj)

            # ---------------- DEAL STAGES ----------------

            stages_data = [
                ("New Deal", 1, False, False, 10),
                ("Negotiation", 2, False, False, 40),
                ("Proposal", 3, False, False, 70),
                ("Won", 4, True, True, 100),
                ("Lost", 5, True, False, 0),
            ]

            deal_stages = []

            for name, order, closed, won, prob in stages_data:

                obj, _ = DealStage.objects.get_or_create(
                    name=name,
                    organization=org,
                    defaults={
                        "order": order,
                        "is_closed": closed,
                        "is_won": won,
                        "probability": prob
                    }
                )

                deal_stages.append(obj)

            self.stdout.write("Pipeline stages ready")

            # ---------------- LEADS ----------------

            leads = []

            for i in range(600):

                company = random.choice(FIRST_NAMES) + " " + random.choice(COMPANY_SUFFIX)

                lead = Lead.objects.create(
                    organization=org,
                    name=company,
                    phone=f"+91-9{random.randint(100000000,999999999)}",
                    email=f"{company.replace(' ','').lower()}{i}@example.com",
                    business_type=random.choice(business_types),
                    source=random.choice(sources),
                    status=random.choice([
                        LeadStatus.NEW,
                        LeadStatus.CALLED,
                        LeadStatus.FOLLOW_UP,
                        LeadStatus.INTERESTED
                    ]),
                    estimated_value=Decimal(random.randint(5000, 500000)),
                    assigned_to=random.choice(sales_users),
                )

                leads.append(lead)

            self.stdout.write("600 leads created")

            # ---------------- ACTIVITIES ----------------

            for lead in leads:

                for _ in range(random.randint(1,4)):

                    Activity.objects.create(
                        organization=org,
                        lead=lead,
                        user=random.choice(sales_users),
                        activity_type=random.choice(activity_types),
                        note=random.choice(NOTES),
                        next_follow_up=timezone.now() + timedelta(days=random.randint(-3,5))
                    )

            self.stdout.write("Activities generated")

            # ---------------- DEALS ----------------

            interested_leads = [l for l in leads if l.status == LeadStatus.INTERESTED]

            for lead in random.sample(interested_leads, min(200, len(interested_leads))):

                stage = random.choice(deal_stages)

                deal = Deal.objects.create(
                    organization=org,
                    lead=lead,
                    stage=stage,
                    value=lead.estimated_value or 50000
                )

                if stage.is_closed:
                    deal.closed_at = timezone.now()
                    deal.closed_by = random.choice(sales_users)
                    deal.save(update_fields=["closed_at","closed_by"])

            self.stdout.write(self.style.SUCCESS("Deals generated"))

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("Demo CRM dataset ready"))
            self.stdout.write("")
            self.stdout.write("LOGIN:")
            self.stdout.write("admin / Admin@123")
            self.stdout.write("sales0 / Sales@123")
        finally:
            clear_system_mode()










