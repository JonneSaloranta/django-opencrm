# opencrm/forms.py
from django import forms

from .models import Company, CompanyType


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "type"]
        widgets = {
            "type": forms.CheckboxSelectMultiple(),
        }
