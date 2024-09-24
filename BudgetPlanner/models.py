from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from Expenses.models import Expense  # Assuming 'expenses' is the app name

class ReportDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_budget = models.FloatField()
    budget_title = models.CharField(default = "NULL", max_length=50)
    education_budget = models.FloatField()
    medical_budget = models.FloatField()
    food_budget = models.FloatField()
    entertainment_budget = models.FloatField()
    transport_budget = models.FloatField()
    personal_care_budget = models.FloatField()
    housing_bills_budget = models.FloatField()

class AiReportDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_weekly_budget = models.FloatField()
    education_budget = models.FloatField()
    medical_budget = models.FloatField()
    food_budget = models.FloatField()
    entertainment_budget = models.FloatField()
    transport_budget = models.FloatField()
    personal_care_budget = models.FloatField()
    housing_bills_budget = models.FloatField()

class AiReportDateM(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_monthly_budget = models.FloatField()
    education_budget = models.FloatField()
    medical_budget = models.FloatField()
    food_budget = models.FloatField()
    entertainment_budget = models.FloatField()
    transport_budget = models.FloatField()
    personal_care_budget = models.FloatField()
    housing_bills_budget = models.FloatField()

class Expense2(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)
    expense = models.ForeignKey(to=Expense, on_delete=models.CASCADE, related_name='linked_expense')

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']
