from django import forms

from .models import Company, CompanyType, Contact, Note, Tag, Task


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "type"]
        widgets = {
            "type": forms.SelectMultiple(attrs={"class": "form-select", "size": "5"})
        }


class CompanyTypeForm(forms.ModelForm):
    class Meta:
        model = CompanyType
        fields = ["name"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["contact", "text", "due_date", "is_done"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["contact", "text"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "firstname",
            "lastname",
            "email",
            "phonenumber",
            "company",
            "tag",
        ]
        widgets = {
            "tag": forms.SelectMultiple(attrs={"class": "form-select", "size": "5"})
        }
