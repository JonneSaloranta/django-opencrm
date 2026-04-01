from datetime import timedelta

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .forms import CompanyForm


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
def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return redirect(company.get_absolute_url())
    else:
        form = CompanyForm()

    return render(request, "opencrm/add_company.html", {"form": form})
