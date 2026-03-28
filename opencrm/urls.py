from django.urls import path

from . import views

app_name = "opencrm"

urlpatterns = [
    path("", views.index, name="index"),
    path("companies", views.companies_view, name="companies"),
    path("company/<int:id>/", views.company_view, name="company_details"),
    path("contact/<int:id>/", views.contact_details, name="contact_details"),
    path("api/search-contacts/", views.contact_search_api, name="contact_search_api"),
]
