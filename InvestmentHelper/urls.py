from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('', views.investment_helper, name="investment_helper"),

]