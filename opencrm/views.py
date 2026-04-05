from datetime import timedelta

from django.contrib import messages
from django.db.models import Count, ProtectedError, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView

from .forms import (CompanyForm, CompanyTypeForm, ContactForm, NoteForm,
                    TagForm, TaskForm)
from .models import Company, CompanyType, Contact, Note, Tag, Task


def index(request):
    context = {}
    return render(request, "opencrm/index.html", context)


def companies_view(request):
    companies = Company.objects.annotate(
        open_task_count=Count('contacts__tasks', filter=Q(contacts__tasks__is_done=False))
    ).order_by('-open_task_count', '-updated_at')

    context = {
        "companies": companies,
    }
    return render(request, "opencrm/all_companies.html", context)


def company_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    context = {
        "company": company,
    }
    return render(request, "opencrm/company_details.html", context)


def contact_details(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    context = {
        "contact": contact,
    }
    return render(request, "opencrm/contact_details.html", context)


def task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {
        "task": task,
    }
    return render(request, "opencrm/task_details.html", context)


def all_tags_api(request):
    tags = Tag.objects.all().values("pk", "name")
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
                "pk": contact.pk,
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
    tasks = Task.objects.order_by("is_done","due_date")
    context = {
        "tasks": tasks,
            "cancel_url": reverse("opencrm:contacts"),
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

    return render(request, "opencrm/add_company.html", {"form": form, "cancel_url": reverse("opencrm:companies"),})


def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect(contact.get_absolute_url())
    else:
        form = ContactForm()

    return render(request, "opencrm/add_contact.html", {"form": form, "cancel_url": reverse("opencrm:contacts"),})


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect(task.get_absolute_url())
    else:
        form = TaskForm()

    return render(request, "opencrm/add_task.html", {"form": form, "cancel_url": reverse("opencrm:tasks")})


def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect(tag.get_absolute_url())
    else:
        form = TagForm()

    return render(request, "opencrm/add_tag.html", {"form": form, "cancel_url": reverse("opencrm:tags")})


def all_tags(request):
    tags = Tag.objects.all()

    context = {"tags": tags}

    return render(request, "opencrm/all_tags.html", context=context)


def tag_details(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

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

    return render(request, "opencrm/add_note.html", {"form": form,    "cancel_url": reverse("opencrm:notes")})


def all_notes(request):
    notes = Note.objects.all()

    context = {"notes": notes}

    return render(request, "opencrm/all_notes.html", context=context)


def note_details(request, pk):
    note = get_object_or_404(Note, pk=pk)

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

    return render(request, "opencrm/add_companytype.html", {"form": form, "cancel_url": reverse("opencrm:companytypes")})


def all_companytypes(request):
    companytypes = CompanyType.objects.all()

    context = {"companytypes": companytypes}

    return render(request, "opencrm/all_companytypes.html", context=context)


def companytype_details(request, pk):
    companytype = get_object_or_404(CompanyType, pk=pk)

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
                "task_id": t.pk,
                "task_text": t.text,
                "task_url": f"/crm/tasks/{t.pk}/",
                "contact_id": t.contact.pk if t.contact else None,
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



class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "opencrm/edit_company.html"

    def get_success_url(self):
        return reverse_lazy("opencrm:company_details", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("opencrm:company_details", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("opencrm:delete_company", kwargs={"pk": self.object.pk})
        return context
    
class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("opencrm:companies")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'"{obj}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, f'"{self.object}" was successfully deleted.')
            return response

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object}" because it has related contacts.'
            )
            return redirect(self.object.get_absolute_url())
    
class CompanytypeUpdateView(UpdateView):
    model = CompanyType
    form_class = CompanyTypeForm
    template_name = "opencrm/edit_companytype.html"

    def get_success_url(self):
        return reverse_lazy("opencrm:companytype_details", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("opencrm:companytype_details", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("opencrm:delete_companytype", kwargs={"pk": self.object.pk})
        return context
    

class CompanyTypeDeleteView(DeleteView):
    model = CompanyType
    success_url = reverse_lazy("opencrm:companytypes")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'"{obj}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, f'"{self.object}" was successfully deleted.')
            return response

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object}" because it has related contacts.'
            )
            return redirect(self.object.get_absolute_url())
    
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "opencrm/edit_note.html"

    def get_success_url(self):
        return reverse_lazy("opencrm:note_details", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("opencrm:note_details", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("opencrm:delete_note", kwargs={"pk": self.object.pk})
        return context
    
    
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy("opencrm:notes")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'"{obj}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, f'"{self.object}" was successfully deleted.')
            return response

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object}" because it has related contacts.'
            )
            return redirect(self.object.get_absolute_url())
    


class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "opencrm/edit_tag.html"

    def get_success_url(self):
        return reverse_lazy("opencrm:tag_details", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("opencrm:tag_details", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("opencrm:delete_tag", kwargs={"pk": self.object.pk})
        return context
    
    
class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy("opencrm:tags")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'"{obj}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, f'"{self.object}" was successfully deleted.')
            return response

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object}" because it has related contacts.'
            )
            return redirect(self.object.get_absolute_url())
    
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "opencrm/edit_task.html"

    def get_success_url(self):
        return reverse_lazy("opencrm:task_details", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("opencrm:task_details", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("opencrm:delete_task", kwargs={"pk": self.object.pk})
        return context
    
    
class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("opencrm:tasks")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'"{obj}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, f'"{self.object}" was successfully deleted.')
            return response

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object}" because it has related contacts.'
            )
            return redirect(self.object.get_absolute_url())
    
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "opencrm/edit_contact.html"

    def get_success_url(self):
        return reverse_lazy("opencrm:contact_details", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("opencrm:contact_details", kwargs={"pk": self.object.pk})
        context["delete_url"] = reverse_lazy("opencrm:delete_contact", kwargs={"pk": self.object.pk})
        return context
    
    
class ContactDeleteView(DeleteView):
    model = Contact
    success_url = reverse_lazy("opencrm:contacts")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'"{obj}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, f'"{self.object}" was successfully deleted.')
            return response

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object}" because it has related contacts.'
            )
            return redirect(self.object.get_absolute_url())