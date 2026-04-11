import datetime

import pytest
from django.forms import ValidationError
from django.urls import reverse

from opencrm.models import Company, CompanyType, Contact, Note, Tag, Task


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
    expected_url = reverse(
        "opencrm:company_details", kwargs={"pk": company.pk}
    )
    assert url == expected_url


@pytest.mark.django_db
def test_company_type_list_property():
    type1 = CompanyType.objects.create(name="company_type 1")
    type2 = CompanyType.objects.create(name="company_type 2")
    type3 = CompanyType.objects.create(name="company_type 3")

    company = Company.objects.create(name="Company")
    company.type.add(type1, type2, type3)
    assert company.type.count() == 3

    type_names = list(company.type.values_list("name", flat=True))

    assert "company_type 1" in type_names
    assert "company_type 2" in type_names
    assert "company_type 3" in type_names


@pytest.mark.django_db
def test_tag_list_empty():
    contact = Contact.objects.create(firstname="John")

    assert contact.tag_list == ""


@pytest.mark.django_db
def test_tag_get_absolute_url():
    tag = Tag.objects.create(name="Test tag")
    url = tag.get_absolute_url()
    expected_url = reverse("opencrm:tag_details", kwargs={"pk": tag.pk})
    assert url == expected_url


@pytest.mark.django_db
def test_tag_list_single():
    contact = Contact.objects.create(firstname="John")
    tag = Tag.objects.create(name="VIP")

    contact.tag.add(tag)

    assert contact.tag_list == "VIP"


@pytest.mark.django_db
def test_tag_list_multiple():
    contact = Contact.objects.create(firstname="John")
    tag1 = Tag.objects.create(name="VIP")
    tag2 = Tag.objects.create(name="Customer")

    contact.tag.add(tag1, tag2)

    result = contact.tag_list

    assert "VIP" in result
    assert "Customer" in result
    assert ", " in result


@pytest.mark.django_db
def test_contact_str():
    company = Company.objects.create(name="My Company")
    contact = Contact.objects.create(
        firstname="John",
        lastname="Doe",
        email="john.doe@email.com",
        company=company,
    )
    assert str(contact) == "John Doe"


@pytest.mark.django_db
def test_contact_tag_list_property():
    tag1 = Tag.objects.create(name="test1")
    tag2 = Tag.objects.create(name="test2")
    tag3 = Tag.objects.create(name="test3")

    contact = Contact.objects.create(firstname="John")
    contact.tag.add(tag1, tag2, tag3)
    assert contact.tag.count() == 3

    tag_names = list(contact.tag.values_list("name", flat=True))

    assert "test1" in tag_names
    assert "test2" in tag_names
    assert "test3" in tag_names


@pytest.mark.django_db
def test_type_list_empty():
    company = Company.objects.create(name="Test")

    assert company.type_list == ""


@pytest.mark.django_db
def test_type_list_single():
    company = Company.objects.create(name="Test")
    t = CompanyType.objects.create(name="Supplier")

    company.type.add(t)

    assert company.type_list == "Supplier"


@pytest.mark.django_db
def test_type_list_multiple_sorted():
    company = Company.objects.create(name="Test")

    t1 = CompanyType.objects.create(name="Customer")
    t2 = CompanyType.objects.create(name="Supplier")
    t3 = CompanyType.objects.create(name="Partner")

    company.type.add(t2, t1, t3)

    assert company.type_list == "Customer, Partner, Supplier"


@pytest.mark.django_db
def test_contact_fullname_property():
    contact = Contact.objects.create(firstname="John")
    assert contact.fullname == "John"
    contact.lastname = "Doe"
    assert contact.fullname == "John Doe"


@pytest.mark.django_db
def test_contact_get_absolute_url():
    contact = Contact.objects.create(firstname="John", lastname="Doe")
    url = contact.get_absolute_url()
    expected_url = reverse(
        "opencrm:contact_details", kwargs={"pk": contact.pk}
    )
    assert url == expected_url


@pytest.mark.django_db
def test_task_get_absolute_url():
    contact = Contact.objects.create(firstname="John", lastname="Doe")
    task = Task.objects.create(contact=contact, text="Hello")
    url = task.get_absolute_url()
    expected_url = reverse("opencrm:task_details", kwargs={"pk": task.pk})
    assert url == expected_url


@pytest.mark.django_db
def test_note_str():
    company = Company.objects.create(name="A company")
    assert company is not None
    assert type(company) is Company
    contact = Contact.objects.create(
        firstname="John", lastname="Doe", company=company
    )
    note = Note.objects.create(contact=contact, text="Hello")
    assert str(note) == "John Doe: Hello"


@pytest.mark.django_db
def test_note_get_absolute_url():
    contact = Contact.objects.create(firstname="John", lastname="Doe")
    note = Note.objects.create(contact=contact, text="Test note")
    url = note.get_absolute_url()
    expected_url = reverse("opencrm:note_details", kwargs={"pk": note.pk})
    assert url == expected_url


@pytest.mark.django_db
def test_tag_str():
    tag = Tag.objects.create(name="This is a test tag")
    assert str(tag) == "This is a test tag"


@pytest.mark.django_db
def test_tag_name_max_length():
    tag = Tag(name="a" * 51)

    with pytest.raises(ValidationError):
        tag.full_clean()


@pytest.mark.django_db
def test_tag_name_max_length_valid():
    tag = Tag(name="a" * 50)

    tag.full_clean()


@pytest.mark.django_db
def test_companytype_str():
    type = CompanyType.objects.create(name="A type")
    assert str(type) == "A type"


@pytest.mark.django_db
def test_companytype_get_absolute_url():
    type = CompanyType.objects.create(name="Test type")
    url = type.get_absolute_url()
    expected_url = reverse(
        "opencrm:companytype_details", kwargs={"pk": type.pk}
    )
    assert url == expected_url


@pytest.mark.django_db
def test_task_str():
    contact = Contact.objects.create(firstname="John", lastname="Doe")
    task = Task.objects.create(contact=contact, text="Hello")

    assert str(task) == "Hello"
