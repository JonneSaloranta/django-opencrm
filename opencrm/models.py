from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CompanyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("opencrm:companytype_details", kwargs={"id": self.id})


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ManyToManyField(
        CompanyType,
        blank=True,
        related_name="company",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("opencrm:company_details", kwargs={"id": self.id})

    @property
    def type_list(self):
        return ", ".join(t.name for t in self.type.all().order_by("name"))

    @property
    def task_count(self):
        return Task.objects.filter(contact__company=self, is_done=False).count()

    @property
    def open_tasks(self):
        return Task.objects.filter(
            contact__company=self, is_done=False
        ).order_by("-due_date")


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("opencrm:tag_details", kwargs={"id": self.id})


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
    tag = models.ManyToManyField(Tag, blank=True, related_name="contact")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.fullname}"

    @property
    def tag_list(self):
        return ", ".join(tag.name for tag in self.tag.all().order_by("name"))

    @property
    def fullname(self):
        if self.firstname and self.lastname:
            return f"{self.firstname} {self.lastname}"
        return f"{self.firstname}"

    def get_absolute_url(self):
        return reverse("opencrm:contact_details", kwargs={"id": self.id})


class Note(models.Model):
    contact = models.ForeignKey(
        Contact,
        verbose_name=_("Contact"),
        on_delete=models.PROTECT,
        related_name="notes",
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact.firstname} {self.contact.lastname}: {self.text}"

    class Meta:
        ordering = ["-updated_at"]

    def get_absolute_url(self):
        return reverse("opencrm:note_details", kwargs={"id": self.id})


class Task(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="tasks")
    text = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        ordering = ["-updated_at"]

    def get_absolute_url(self):
        return reverse("opencrm:task_details", kwargs={"id": self.id})
