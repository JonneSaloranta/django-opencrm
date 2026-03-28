from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Contact, Note, Task


@receiver(post_save, sender=Note)
def update_last_contacted_from_note(sender, instance, **kwargs):
    contact = instance.contact
    contact.last_contacted = instance.created_at
    contact.save(update_fields=["last_contacted"])


@receiver(post_save, sender=Task)
def update_last_contacted_from_task(sender, instance, **kwargs):
    if instance.is_done:
        contact = instance.contact
        contact.last_contacted = timezone.now()
        contact.save(update_fields=["last_contacted"])
