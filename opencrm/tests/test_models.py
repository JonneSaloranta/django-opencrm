import datetime

import pytest
from django.urls import reverse

from opencrm.models import Company, Contact, Note, Tag


@pytest.mark.django_db
def test_company_str():
    company = Company.objects.create(name="My Company")
    assert str(company) == "My Company"


@pytest.mark.django_db
def test_company_create_update_datetime_is_update():
    company = Company.objects.create(name="My Company")
    assert company.created_at is not None
    assert company.updated_at is not None
    assert type(company.created_at) is datetime.datetime
    assert type(company.updated_at) is datetime.datetime


@pytest.mark.django_db
def test_company_get_absolute_url():
    company = Company.objects.create(name="Test Company")
    url = company.get_absolute_url()
    expected_url = reverse("opencrm:company_details", kwargs={"id": company.id})
    assert url == expected_url


@pytest.mark.django_db
def test_contact_str():
    company = Company.objects.create(name="My Company")
    contact = Contact.objects.create(
        firstname="John", lastname="Doe", email="john.doe@email.com", company=company
    )
    assert str(contact) == "My Company - John Doe"


@pytest.mark.django_db
def test_note_str():
    company = Company.objects.create(name="A company")
    assert company is not None
    assert type(company) is Company
    contact = Contact.objects.create(firstname="John", lastname="Doe", company=company)
    note = Note.objects.create(contact=contact, text="Hello")
    assert str(note) == "John Doe: Hello"


@pytest.mark.django_db
def test_tag_str():
    tag = Tag.objects.create(name="This is a test tag")
    assert str(tag) == "This is a test tag"

