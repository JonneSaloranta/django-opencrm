import pytest
from django.utils import timezone

from opencrm.models import Contact, Note, Task


@pytest.mark.django_db
def test_note_updates_last_contacted():
    contact = Contact.objects.create(firstname="John")

    note = Note.objects.create(
        contact=contact,
        text="Test note",
    )

    contact.refresh_from_db()

    assert contact.last_contacted == note.created_at


@pytest.mark.django_db
def test_task_done_updates_last_contacted():
    contact = Contact.objects.create(firstname="John")

    before = timezone.now()

    task = Task.objects.create(
        contact=contact,
        text="Call client",
    )

    task.is_done = True

    task.save()

    contact.refresh_from_db()

    assert contact.last_contacted is not None
    assert contact.last_contacted >= before


@pytest.mark.django_db
def test_task_not_done_does_not_update_last_contacted():
    contact = Contact.objects.create(firstname="John")

    Task.objects.create(
        contact=contact,
        text="Call client",
        is_done=False,
    )

    contact.refresh_from_db()

    assert contact.last_contacted is None
