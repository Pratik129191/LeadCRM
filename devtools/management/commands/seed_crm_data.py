import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User, Organization
from leads.models import Lead, BusinessType, LeadSource
from activities.models import Activity, ActivityType
from deals.models import DealStage, Deal
from core.constants import LeadStatus


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

    help = "Create a large realistic CRM demo dataset"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Creating admin user...")

        admin = User.objects.create_user(
            username="admin",
            password="Admin@123",
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
            is_active_member=True
        )

        org = Organization.objects.create(
            name="Demo CRM Organization",
            owner=admin
        )

        admin.organization = org
        admin.save(update_fields=["organization"])

        # SALES USERS
        self.stdout.write("Creating sales team...")

        sales_users = []

        for i in range(8):

            user = User.objects.create_user(
                username=f"sales{i}",
                password="Sales@123",
                role=User.Role.SALES,
                organization=org,
                is_active_member=True
            )

            sales_users.append(user)

        # BUSINESS TYPES
        bt_names = [
            "Restaurant","Retail","Gym","Hospital",
            "Real Estate","School","Salon","Clinic",
            "Hotel","Startup"
        ]

        business_types = [
            BusinessType.objects.create(name=name, organization=org)
            for name in bt_names
        ]

        # SOURCES
        source_names = [
            "Facebook Ads",
            "Google Ads",
            "Website",
            "Cold Call",
            "LinkedIn",
            "Referral",
            "Trade Show",
            "Instagram"
        ]

        sources = [
            LeadSource.objects.create(name=name, organization=org)
            for name in source_names
        ]

        # ACTIVITY TYPES
        activity_types_data = [
            ("Call", True, LeadStatus.CALLED),
            ("Follow Up", True, LeadStatus.FOLLOW_UP),
            ("Interested", True, LeadStatus.INTERESTED),
            ("Proposal Sent", True, LeadStatus.PROPOSAL_SENT),
            ("Negotiation", False, None),
            ("Meeting", False, None),
            ("Note", False, None),
        ]

        activity_types = []

        for name, affects, status in activity_types_data:
            activity_types.append(
                ActivityType.objects.create(
                    name=name,
                    organization=org,
                    affects_pipeline=affects,
                    pipeline_status=status
                )
            )

        # DEAL STAGES
        stages_data = [
            ("New Deal", 1, False, False),
            ("Negotiation", 2, False, False),
            ("Proposal", 3, False, False),
            ("Won", 4, True, True),
            ("Lost", 5, True, False)
        ]

        deal_stages = []

        for name, order, closed, won in stages_data:

            deal_stages.append(
                DealStage.objects.create(
                    name=name,
                    order=order,
                    organization=org,
                    is_closed=closed,
                    is_won=won
                )
            )

        # LEADS
        self.stdout.write("Generating 1000 leads...")

        leads = []

        for i in range(1000):

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
                estimated_value=Decimal(random.randint(10000,500000)),
                assigned_to=random.choice(sales_users)
            )

            leads.append(lead)

        # ACTIVITIES
        self.stdout.write("Generating activities...")

        activities_created = 0

        for lead in leads:

            activity_count = random.randint(1,4)

            for _ in range(activity_count):

                Activity.objects.create(
                    organization=org,
                    lead=lead,
                    user=random.choice(sales_users),
                    activity_type=random.choice(activity_types),
                    note=random.choice(NOTES),
                    next_follow_up=timezone.now()
                )

                activities_created += 1

        # DEALS
        self.stdout.write("Generating deals...")

        interested_leads = [l for l in leads if l.status == LeadStatus.INTERESTED]

        deal_count = min(250, len(interested_leads))

        for lead in random.sample(interested_leads, deal_count):

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

        self.stdout.write(self.style.SUCCESS("Demo CRM dataset created"))

        self.stdout.write("")
        self.stdout.write("LOGIN")
        self.stdout.write("admin / Admin@123")
        self.stdout.write("sales0 / Sales@123")

