from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("opencrm:company_details", kwargs={"id": self.id})


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    firstname = models.CharField()
    lastname = models.CharField(blank=True)
    email = models.EmailField(blank=True)
    phonenumber = models.CharField(blank=True)
    company = models.ForeignKey(
        Company,
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contacts",
    )
    last_contacted = models.DateTimeField(null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.fullname}"

    @property
    def tag_list(self):
        return ", ".join(tag.name for tag in self.tag.all())

    @property
    def fullname(self):
        if self.firstname and self.lastname:
            return f"{self.firstname} {self.lastname}"
        return f"{self.firstname}"

    def get_absolute_url(self):
        return reverse("opencrm:contact_details", kwargs={"id": self.id})


class Note(models.Model):
    contact = models.ForeignKey(
        Contact, verbose_name=_("Contact"), on_delete=models.PROTECT
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact.firstname} {self.contact.lastname}: {self.text}"


class Task(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="tasks")
    text = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"

