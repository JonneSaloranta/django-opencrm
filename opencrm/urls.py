from django.urls import path

from . import views

app_name = "opencrm"

urlpatterns = [
    path("", views.index, name="index"),
    path("companies", views.companies_view, name="companies"),
    path("company/<int:id>/", views.company_view, name="company_details"),
]
