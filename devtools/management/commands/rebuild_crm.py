import os
import shutil
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Completely rebuild CRM database, migrations, and seed demo data"

    def handle(self, *args, **kwargs):

        base_dir = Path(__file__).resolve().parents[3]
        db_path = base_dir / "db.sqlite3"

        apps = [
            "accounts",
            "core",
            "leads",
            "activities",
            "deals",
            "tasks"
        ]

        self.stdout.write(self.style.WARNING("\nRebuilding CRM...\n"))

        # ---------------- DELETE DATABASE ----------------
        if db_path.exists():
            os.remove(db_path)
            self.stdout.write("Deleted db.sqlite3")

        # ---------------- CLEAN MIGRATIONS ----------------
        self.stdout.write("\nCleaning migration files...\n")

        for app in apps:

            migrations_dir = base_dir / app / "migrations"

            if migrations_dir.exists():
                shutil.rmtree(migrations_dir)
                self.stdout.write(f"Removed migrations folder → {app}")

            # recreate clean migrations folder
            migrations_dir.mkdir()

            init_file = migrations_dir / "__init__.py"
            init_file.touch()

            self.stdout.write(f"Recreated migrations folder → {app}")

        # ---------------- REMOVE __pycache__ ----------------
        for root, dirs, files in os.walk(base_dir):
            for d in dirs:
                if d == "__pycache__":
                    shutil.rmtree(os.path.join(root, d))

        self.stdout.write("Removed __pycache__")

        # ---------------- MAKEMIGRATIONS ----------------
        self.stdout.write("\nCreating migrations...\n")

        for app in apps:
            subprocess.run(
                ["python", "manage.py", "makemigrations", app],
                check=True
            )

            self.stdout.write(f"Created migrations for {app}")

        # ---------------- MIGRATE ----------------
        self.stdout.write("\nRunning migrate...\n")
        subprocess.run(
            ["python", "manage.py", "migrate"],
            check=True
        )

        # ---------------- SEED DATA ----------------
        self.stdout.write("\nSeeding demo data...\n")
        subprocess.run(
            ["python", "manage.py", "seed_crm_data"],
            check=True
        )

        self.stdout.write(self.style.SUCCESS("\nCRM rebuild complete.\n"))


