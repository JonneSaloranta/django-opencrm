from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Company, Contact


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


def contact_search_api(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        contacts = Contact.objects.filter(
            Q(firstname__icontains=query)
            | Q(lastname__icontains=query)
            | Q(email__icontains=query)
            | Q(phonenumber__icontains=query)
            | Q(company__name__icontains=query)
            | Q(tag__name__icontains=query)
        ).distinct()[
            :10
        ]  # limit results for performance

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
