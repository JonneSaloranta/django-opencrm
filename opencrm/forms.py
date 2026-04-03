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
