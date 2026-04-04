from datetime import timedelta

import pytest
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from opencrm.models import Company, Contact, Tag, Task


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse("opencrm:index"))
    assert response.status_code == 200
    assert "opencrm/index.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_companies_view(client):
    Company.objects.create(name="A")
    Company.objects.create(name="B")

    response = client.get(reverse("opencrm:companies"))

    assert response.status_code == 200
    assert "companies" in response.context
    assert len(response.context["companies"]) == 2


@pytest.mark.django_db
def test_company_view(client):
    company = Company.objects.create(name="TestCo")

    response = client.get(
        reverse("opencrm:company_details", args=[company.id])
    )

    assert response.status_code == 200
    assert response.context["company"] == company


@pytest.mark.django_db
def test_company_view_404(client):
    response = client.get(reverse("opencrm:company_details", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_contact_details_view(client):
    contact = Contact.objects.create(firstname="John")

    response = client.get(
        reverse("opencrm:contact_details", args=[contact.id])
    )

    assert response.status_code == 200
    assert response.context["contact"] == contact


@pytest.mark.django_db
def test_all_tags_api(client):
    Tag.objects.create(name="VIP")
    Tag.objects.create(name="Customer")

    response = client.get(reverse("opencrm:all_tags_api"))

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert any(tag["name"] == "VIP" for tag in data)


@pytest.mark.django_db
def test_contacts_view(client):
    Contact.objects.create(firstname="John")
    Contact.objects.create(firstname="Jane")

    response = client.get(reverse("opencrm:contacts"))

    assert response.status_code == 200
    assert len(response.context["contacts"]) == 2


# ------------------------
# CONTACT SEARCH API TESTS
# ------------------------


@pytest.mark.django_db
def test_contact_search_basic_query(client):
    Contact.objects.create(firstname="John", lastname="Doe")
    Contact.objects.create(firstname="Jane", lastname="Smith")

    response = client.get(reverse("opencrm:contact_search_api"), {"q": "John"})
    data = response.json()

    assert len(data) == 1
    assert data[0]["fullname"] == "John Doe"


@pytest.mark.django_db
def test_contact_search_by_company(client):
    company = Company.objects.create(name="Acme")
    Contact.objects.create(firstname="John", company=company)

    response = client.get(reverse("opencrm:contact_search_api"), {"q": "Acme"})
    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Acme"


@pytest.mark.django_db
def test_contact_search_by_tag(client):
    tag = Tag.objects.create(name="VIP")
    contact = Contact.objects.create(firstname="John")
    contact.tag.add(tag)

    response = client.get(reverse("opencrm:contact_search_api"), {"q": "VIP"})
    data = response.json()

    assert len(data) == 1
    assert "VIP" in data[0]["tags"]


@pytest.mark.django_db
def test_contact_search_has_open_tasks(client):
    contact = Contact.objects.create(firstname="John")
    Task.objects.create(contact=contact, text="Task", is_done=False)

    response = client.get(
        reverse("opencrm:contact_search_api"), {"has_open_tasks": "1"}
    )
    data = response.json()

    assert len(data) == 1


@pytest.mark.django_db
def test_contact_search_not_contacted_days(client):
    Contact.objects.create(
        firstname="John",
        last_contacted=timezone.now() - timedelta(days=10),
    )

    response = client.get(
        reverse("opencrm:contact_search_api"),
        {"not_contacted_days": "5"},
    )
    data = response.json()

    assert len(data) == 1


@pytest.mark.django_db
def test_contact_search_invalid_not_contacted_days(client):
    Contact.objects.create(firstname="John")

    response = client.get(
        reverse("opencrm:contact_search_api"),
        {"not_contacted_days": "invalid"},
    )

    assert response.status_code == 200  # should not crash


@pytest.mark.django_db
def test_contact_search_filter_by_tag_param(client):
    tag = Tag.objects.create(name="VIP")
    contact = Contact.objects.create(firstname="John")
    contact.tag.add(tag)

    response = client.get(
        reverse("opencrm:contact_search_api"),
        {"tag": "VIP"},
    )
    data = response.json()

    assert len(data) == 1


@pytest.mark.django_db
def test_contact_search_limit_results(client):
    for i in range(15):
        Contact.objects.create(firstname=f"User{i}")

    response = client.get(reverse("opencrm:contact_search_api"))
    data = response.json()

    assert len(data) == 10  # limited to 10


@pytest.mark.django_db
def test_contact_search_response_fields(client):
    Contact.objects.create(
        firstname="John",
        lastname="Doe",
        email="john@example.com",
        phonenumber="123",
    )

    response = client.get(reverse("opencrm:contact_search_api"))
    data = response.json()

    result = data[0]

    assert "pk" in result
    assert "fullname" in result
    assert "email" in result
    assert "phonenumber" in result
    assert "company" in result
    assert "tags" in result
    assert "created_at" in result
    assert "updated_at" in result


@pytest.mark.django_db
def test_task_details_view_get_object_or_404(client):
    contact = Contact.objects.create(firstname="John")
    task = Task.objects.create(contact=contact, text="Hello")

    result = get_object_or_404(Task, id=task.id)
    assert result == task

    with pytest.raises(Http404):
        get_object_or_404(Contact, id=999)


@pytest.mark.django_db
def test_task_details_view_return_correct_template(client):
    contact = Contact.objects.create(firstname="John")
    task = Task.objects.create(contact=contact, text="Hello")

    response = client.get(reverse("opencrm:task_details", args=[task.id]))
    assert response.status_code == 200
    assert "opencrm/task_details.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_all_tasks_view_return_correct_template(client):
    contact = Contact.objects.create(firstname="John")
    Task.objects.create(contact=contact, text="Hello")

    response = client.get(reverse("opencrm:tasks"))
    assert response.status_code == 200
    assert "opencrm/all_tasks.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_upcoming_tasks_api_returns_tasks(client):
    contact = Contact.objects.create(firstname="John", lastname="Doe")

    task = Task.objects.create(
        text="Call client",
        contact=contact,
        is_done=False,
    )

    response = client.get(reverse("opencrm:upcoming_tasks"))

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

    item = data[0]
    assert item["task_id"] == task.id
    assert item["task_text"] == "Call client"
    assert item["contact_id"] == contact.id
    assert item["contact_name"] == "John Doe"


@pytest.mark.django_db
def test_upcoming_tasks_api_excludes_done_tasks(client):
    contact = Contact.objects.create(firstname="John")
    Task.objects.create(contact=contact, text="Done task", is_done=True)
    Task.objects.create(contact=contact, text="Pending task", is_done=False)

    response = client.get(reverse("opencrm:upcoming_tasks"))
    data = response.json()

    assert len(data) == 1
    assert data[0]["task_text"] == "Pending task"


@pytest.mark.django_db
def test_upcoming_tasks_api_limits_to_10(client):
    contact = Contact.objects.create(firstname="John")
    for i in range(15):
        Task.objects.create(contact=contact, text=f"Task {i}", is_done=False)

    response = client.get(reverse("opencrm:upcoming_tasks"))
    data = response.json()

    assert len(data) == 10


@pytest.mark.django_db
def test_upcoming_tasks_api_orders_by_due_date(client):
    contact = Contact.objects.create(firstname="John")
    t1 = Task.objects.create(
        contact=contact,
        text="Later",
        due_date=timezone.now() + timedelta(days=2),
        is_done=False,
    )
    t2 = Task.objects.create(
        contact=contact,
        text="Sooner",
        due_date=timezone.now() + timedelta(days=1),
        is_done=False,
    )

    response = client.get(reverse("opencrm:upcoming_tasks"))
    data = response.json()

    assert data[0]["task_id"] == t2.id
    assert data[1]["task_id"] == t1.id


@pytest.mark.django_db
def test_upcoming_tasks_api_due_date_format(client):
    contact = Contact.objects.create(firstname="John")
    Task.objects.create(
        contact=contact,
        text="With due date",
        due_date=timezone.now(),
        is_done=False,
    )

    response = client.get(reverse("opencrm:upcoming_tasks"))
    data = response.json()

    assert "T" in data[0]["due_date"]


@pytest.mark.django_db
def test_add_company_get(client):
    response = client.get(reverse("opencrm:add_company"))

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_add_company_post_valid(client):
    data = {
        "name": "Test Company",
        # add other required fields here
    }

    response = client.post(reverse("opencrm:add_company"), data)

    # Company created
    company = Company.objects.get(name="Test Company")

    # Redirect to get_absolute_url
    assert response.status_code == 302
    assert response.url == company.get_absolute_url()


@pytest.mark.django_db
def test_add_company_post_invalid(client):
    data = {
        "name": "",
    }

    response = client.post(reverse("opencrm:add_company"), data)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors


@pytest.mark.django_db
def test_add_company_invalid_does_not_create(client):
    client.post(reverse("opencrm:add_company"), {"name": ""})

    assert Company.objects.count() == 0


@pytest.mark.django_db
def test_add_company_template_used(client):
    response = client.get(reverse("opencrm:add_company"))

    assert "opencrm/add_company.html" in [t.name for t in response.templates]
