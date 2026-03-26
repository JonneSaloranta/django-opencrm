from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    firstname = models.CharField()
    lastname = models.CharField(blank=True)
    email = models.EmailField(blank=True)
    phonenumber = models.CharField(blank=True)
    company = models.ForeignKey(
        Company, verbose_name=_("Company"), on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return f"{self.company} - {self.firstname} {self.lastname} "


class Note(models.Model):
    contact = models.ForeignKey(
        Contact, verbose_name=_("Contact"), on_delete=models.PROTECT
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact.firstname} {self.contact.lastname}: {self.text}"
