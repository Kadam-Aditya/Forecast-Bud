
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('',include('Expenses.urls')),
    path('authentication/', include('Authentication.urls')),
    path('preferences/', include('UserPreferences.urls')),
    path('income/', include('Income.urls')),
    path('Budget Planner/', include('BudgetPlanner.urls')),
    path('Finance News/', include('FinanceNews.urls')),
    path('admin/', admin.site.urls),
]
