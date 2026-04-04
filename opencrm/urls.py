from django.urls import path

from . import views

app_name = "opencrm"

urlpatterns = [
    path("", views.index, name="index"),
    path("companies/", views.companies_view, name="companies"),
    path("company/add/", views.add_company, name="add_company"),
    path("company/<int:id>/", views.company_view, name="company_details"),
    path("company/<int:pk>/edit/", views.CompanyUpdateView.as_view(), name="edit_company"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("contacts/add/", views.add_contact, name="add_contact"),
    path("contact/<int:id>/", views.contact_details, name="contact_details"),
    path("tasks/", views.all_tasks, name="tasks"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:id>/", views.task_details, name="task_details"),
    path("tags/", views.all_tags, name="tags"),
    path("tags/add/", views.add_tag, name="add_tag"),
    path("tags/<int:id>/", views.tag_details, name="tag_details"),
    path("notes/", views.all_notes, name="notes"),
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/<int:id>/", views.note_details, name="note_details"),
    path("companytypes/", views.all_companytypes, name="companytypes"),
    path("companytypes/add/", views.add_companytype, name="add_companytype"),
    path(
        "companytypes/<int:id>/",
        views.companytype_details,
        name="companytype_details",
    ),
    path("api/tags/", views.all_tags_api, name="all_tags_api"),
    path(
        "api/search-contacts/",
        views.contact_search_api,
        name="contact_search_api",
    ),
    path("api/upcoming-tasks/", views.upcoming_tasks_api, name="upcoming_tasks"),
]
