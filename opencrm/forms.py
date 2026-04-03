# opencrm/forms.py
from django import forms

from .models import Company, CompanyType, Contact, Note, Tag, Task


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "type"]
        widgets = {
            "type": forms.CheckboxSelectMultiple(),
        }


class CompanyTypeForm(forms.ModelForm):
    class Meta:
        model = CompanyType
        fields = ["name"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["contact", "text"]

