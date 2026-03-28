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
