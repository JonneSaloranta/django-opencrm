from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Note, Task


@receiver(post_save, sender=Note)
def update_last_contacted_from_note(sender, instance, **kwargs):
    contact = instance.contact
    contact.last_contacted = instance.created_at
    contact.save(update_fields=["last_contacted"])


@receiver(pre_save, sender=Task)
def update_last_contacted_from_task(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_task = Task.objects.get(pk=instance.pk)
    if not old_task.is_done and instance.is_done:
        contact = instance.contact
        contact.last_contacted = timezone.now()
        contact.save(update_fields=["last_contacted"])
