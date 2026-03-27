from django.contrib import admin

from .models import Company, Contact, Note


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_at",
        "updated_at",
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "firstname",
        "lastname",
        "email",
        "phonenumber",
        "company",
        "last_contacted",
        "tag",
    ]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        "contact",
        "text",
        "created_at",
        "updated_at",
    ]
