# Expenses/management/commands/seed_expenses.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Expenses.models import Expense
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = "Seed database with 5 years of realistic expenses"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="Aditya Kadam",
            defaults={"email": "work.adityakadam@gmail.com"}
        )

        if created:
            user.set_password("Aadiii@292752")
            user.save()
            self.stdout.write(self.style.SUCCESS("Created test user"))

        categories = {
            "Food": (100, 500),
            "Transport": (50, 300),
            "Entertainment": (200, 1500),
            "Medical": (100, 2000),
            "Education": (500, 5000),
            "Personal care": (100, 800),
            "Housing/Bills": (2000, 10000),
        }

        # ⚠️ Clear old data
        Expense.objects.filter(owner=user).delete()

        today = datetime.today()
        start_date = today - timedelta(days=5 * 365)  # 5 years

        expenses_created = []

        current_date = start_date

        while current_date <= today:
            for category, (min_amt, max_amt) in categories.items():

                # Frequency logic (more realistic)
                if category == "Housing/Bills":
                    # monthly
                    if current_date.day != 1:
                        continue

                elif category == "Education":
                    # occasional
                    if random.random() > 0.1:
                        continue

                elif category == "Medical":
                    if random.random() > 0.2:
                        continue

                else:
                    # daily categories
                    if random.random() > 0.7:
                        continue

                expense = Expense(
                    owner=user,
                    amount=random.randint(min_amt, max_amt),
                    category=category,
                    date=current_date,
                    description=f"{category} expense"
                )

                expenses_created.append(expense)

            current_date += timedelta(days=1)

        # Bulk insert
        Expense.objects.bulk_create(expenses_created, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(expenses_created)} expenses over 5 years"))