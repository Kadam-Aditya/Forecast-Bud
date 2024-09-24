from django.urls import path
from . import views
from .views import generate_report_view, ai_view, saved_budgets_view, saved_budgets_view1, delete_budget, budget_planner, ai_saved_budgets_view, ai_saved_budgets_view_m
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('', views.index, name="Budget Planner"),
    path('Budget Planner/ai_budget', ai_view,name="ai_budget"),
    path('Budget Planner/ai_budget_result', budget_planner,name="ai_budget_result"),
    path('Budget Planner/ai_weekly_result', budget_planner,name="ai_weekly_result"),
    path('Budget Planner/saved_ai_weekly_result', ai_saved_budgets_view,name="saved_ai_weekly_result"),
    path('Budget Planner/saved_ai_monthly_result', ai_saved_budgets_view_m,name="saved_ai_monthly_result"),
    path('Budget Planner/ai_monthly_result', budget_planner,name="ai_monthly_result"),
    path('Budget Planner/budget', generate_report_view,name="budget"),
    path('Budget Planner/Saved Budgets', saved_budgets_view, name="Saved Budgets"),
    path('Budget Planner/Saved Budgets1', saved_budgets_view1, name="Saved Budgets1"),
    path('delete_budget/<int:budget_id>/', delete_budget, name='delete_budget'),
    path('edit_budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
]