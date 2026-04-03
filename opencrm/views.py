from datetime import timedelta

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    CompanyForm,
    CompanyTypeForm,
    ContactForm,
    NoteForm,
    TagForm,
    TaskForm,
)
from .models import Company, CompanyType, Contact, Note, Tag, Task


def index(request):
    context = {}
    return render(request, "opencrm/index.html", context)


def companies_view(request):
    companies = Company.objects.all().order_by("-updated_at")
    context = {
        "companies": companies,
    }
    return render(request, "opencrm/all_companies.html", context)


def company_view(request, id):
    company = get_object_or_404(Company, id=id)
    context = {
        "company": company,
    }
    return render(request, "opencrm/company_details.html", context)


def contact_details(request, id):
    contact = get_object_or_404(Contact, id=id)
    context = {
        "contact": contact,
    }
    return render(request, "opencrm/contact_details.html", context)


def task_details(request, id):
    task = get_object_or_404(Task, id=id)
    context = {
        "task": task,
    }
    return render(request, "opencrm/task_details.html", context)


def all_tags_api(request):
    tags = Tag.objects.all().values("id", "name")
    return JsonResponse(list(tags), safe=False)


def contact_search_api(request):
    query = request.GET.get("q", "")
    results = []

    contacts = Contact.objects.all()

    # --- Search query ---
    if query:
        contacts = contacts.filter(
            Q(firstname__icontains=query)
            | Q(lastname__icontains=query)
            | Q(email__icontains=query)
            | Q(phonenumber__icontains=query)
            | Q(company__name__icontains=query)
            | Q(tag__name__icontains=query)
        ).distinct()

    # --- Filter: has open tasks ---
    if request.GET.get("has_open_tasks"):
        contacts = contacts.filter(tasks__is_done=False).distinct()

    # --- Filter: not contacted in X days ---
    not_contacted_days = request.GET.get("not_contacted_days")
    if not_contacted_days:
        try:
            days = int(not_contacted_days)
            cutoff = timezone.now() - timedelta(days=days)
            contacts = contacts.filter(
                Q(last_contacted__lt=cutoff) | Q(last_contacted__isnull=True)
            )
        except ValueError:
            pass  # ignore invalid input

    # --- Filter: tag ---
    tag = request.GET.get("tag")
    if tag:
        contacts = contacts.filter(tag__name=tag)

    # Limit results for performance
    contacts = contacts.distinct()[:10]

    # --- Build JSON response ---
    for contact in contacts:
        results.append(
            {
                "id": contact.id,
                "fullname": f"{contact.firstname} {contact.lastname}",
                "contact_url": contact.get_absolute_url(),
                "email": contact.email,
                "phonenumber": contact.phonenumber or "",
                "company": contact.company.name if contact.company else "",
                "company_url": (
                    contact.company.get_absolute_url() if contact.company else ""
                ),
                "tags": [t.name for t in contact.tag.all()],
                "last_contacted": (
                    contact.last_contacted.isoformat()
                    if contact.last_contacted
                    else None
                ),
                "created_at": (
                    contact.created_at.isoformat() if contact.created_at else None
                ),
                "updated_at": (
                    contact.updated_at.isoformat() if contact.updated_at else None
                ),
            }
        )

    return JsonResponse(results, safe=False)


def contacts_view(request):
    contacts = Contact.objects.all()
    context = {
        "contacts": contacts,
    }
    return render(request, "opencrm/all_contacts.html", context)


def all_tasks(request):
    tasks = Task.objects.all().order_by("-due_date")
    context = {
        "tasks": tasks,
    }
    return render(request, "opencrm/all_tasks.html", context)


def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return redirect(company.get_absolute_url())
    else:
        form = CompanyForm()

    return render(request, "opencrm/add_company.html", {"form": form})


def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect(contact.get_absolute_url())
    else:
        form = ContactForm()

    return render(request, "opencrm/add_contact.html", {"form": form})


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect(task.get_absolute_url())
    else:
        form = TaskForm()

    return render(request, "opencrm/add_task.html", {"form": form})


def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect(tag.get_absolute_url())
    else:
        form = TagForm()

    return render(request, "opencrm/add_tag.html", {"form": form})


def all_tags(request):
    tags = Tag.objects.all()

    context = {"tags": tags}

    return render(request, "opencrm/all_tags.html", context=context)


def tag_details(request, id):
    tag = get_object_or_404(Tag, id=id)

    context = {
        "tag": tag,
    }
    return render(request, "opencrm/tag_details.html", context)


def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            return redirect(note.get_absolute_url())
    else:
        form = NoteForm()

    return render(request, "opencrm/add_note.html", {"form": form})


def all_notes(request):
    notes = Note.objects.all()

    context = {"notes": notes}

    return render(request, "opencrm/all_notes.html", context=context)


def note_details(request, id):
    note = get_object_or_404(Note, id=id)

    context = {
        "note": note,
    }
    return render(request, "opencrm/note_details.html", context)


def add_companytype(request):
    if request.method == "POST":
        form = CompanyTypeForm(request.POST)
        if form.is_valid():
            compantytype = form.save()
            return redirect(compantytype.get_absolute_url())
    else:
        form = CompanyTypeForm()

    return render(request, "opencrm/add_companytype.html", {"form": form})


def all_companytypes(request):
    companytypes = CompanyType.objects.all()

    context = {"companytypes": companytypes}

    return render(request, "opencrm/all_companytypes.html", context=context)


def companytype_details(request, id):
    companytype = get_object_or_404(CompanyType, id=id)

    context = {
        "companytype": companytype,
    }
    return render(request, "opencrm/companytype_details.html", context)


def upcoming_tasks_api(request):
    tasks = (
        Task.objects.filter(is_done=False)
        .order_by("due_date")[:10]
        .select_related("contact")  # faster join for contact
    )

    results = []
    for t in tasks:
        results.append(
            {
                "task_id": t.id,
                "task_text": t.text,
                "task_url": f"/crm/tasks/{t.id}/",
                "contact_id": t.contact.id if t.contact else None,
                "contact_name": (
                    f"{t.contact.firstname} {t.contact.lastname}"
                    if t.contact
                    else "No contact"
                ),
                "contact_url": (t.contact.get_absolute_url() if t.contact else "#"),
                "due_date": t.due_date.isoformat() if t.due_date else None,
            }
        )

    return JsonResponse(results, safe=False)
