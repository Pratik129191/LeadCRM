from django import forms

from accounts.models import User
from .models import Lead, BusinessType, LeadSource


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead

        fields = [
            "name",
            "phone",
            "email",
            "business_type",
            "status",
            "estimated_value",
            "assigned_to",
            "notes",
            "source",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "business_type": forms.Select(
                attrs={"class": "form-control"}
            ),

            "status": forms.Select(
                attrs={"class": "form-control"}
            ),

            "estimated_value": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "assigned_to": forms.Select(
                attrs={"class": "form-control"}
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['business_type'].queryset = BusinessType.objects.filter(
                organization=user.organization
            )

            self.fields['source'].queryset = LeadSource.objects.filter(
                organization=user.organization
            )

            self.fields['assigned_to'].queryset = User.objects.filter(
                organization=user.organization,
                role=user.Role.SALES
            )

            if user.role == User.Role.SALES:
                self.fields.pop('assigned_to')
