from django.urls import path

from . import views

app_name = "opencrm"

urlpatterns = [
    path("", views.index, name="index"),
    path("companies/", views.companies_view, name="companies"),
    path("companies/add/", views.add_company, name="add_company"),
    path("companies/<int:pk>/", views.company_view, name="company_details"),
    path(
        "companies/<int:pk>/edit/",
        views.CompanyUpdateView.as_view(),
        name="edit_company",
    ),
    path(
        "companies/<int:pk>/delete/",
        views.CompanyDeleteView.as_view(),
        name="delete_company",
    ),
    path("contacts/", views.contacts_view, name="contacts"),
    path("contacts/add/", views.add_contact, name="add_contact"),
    path("contacts/<int:pk>/", views.contact_details, name="contact_details"),
    path(
        "contacts/<int:pk>/edit/",
        views.ContactUpdateView.as_view(),
        name="edit_contact",
    ),
    path(
        "contacts/<int:pk>/delete/",
        views.ContactDeleteView.as_view(),
        name="delete_contact",
    ),
    path("tasks/", views.all_tasks, name="tasks"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:pk>/", views.task_details, name="task_details"),
    path(
        "tasks/<int:pk>/edit/",
        views.TaskUpdateView.as_view(),
        name="edit_task",
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="delete_task",
    ),
    path("tags/", views.all_tags, name="tags"),
    path("tags/add/", views.add_tag, name="add_tag"),
    path("tags/<int:pk>/", views.tag_details, name="tag_details"),
    path(
        "tags/<int:pk>/edit/", views.TagUpdateView.as_view(), name="edit_tag"
    ),
    path(
        "tags/<int:pk>/delete/",
        views.TagDeleteView.as_view(),
        name="delete_tag",
    ),
    path("notes/", views.all_notes, name="notes"),
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/<int:pk>/", views.note_details, name="note_details"),
    path(
        "notes/<int:pk>/edit/",
        views.NoteUpdateView.as_view(),
        name="edit_note",
    ),
    path(
        "notes/<int:pk>/delete/",
        views.NoteDeleteView.as_view(),
        name="delete_note",
    ),
    path("companytypes/", views.all_companytypes, name="companytypes"),
    path("companytypes/add/", views.add_companytype, name="add_companytype"),
    path(
        "companytypes/<int:pk>/",
        views.companytype_details,
        name="companytype_details",
    ),
    path(
        "companytypes/<int:pk>/edit/",
        views.CompanytypeUpdateView.as_view(),
        name="edit_companytype",
    ),
    path(
        "companytype/<int:pk>/delete/",
        views.CompanyTypeDeleteView.as_view(),
        name="delete_companytype",
    ),
    path("api/tags/", views.all_tags_api, name="all_tags_api"),
    path(
        "api/search-contacts/",
        views.contact_search_api,
        name="contact_search_api",
    ),
    path(
        "api/upcoming-tasks/", views.upcoming_tasks_api, name="upcoming_tasks"
    ),
]
