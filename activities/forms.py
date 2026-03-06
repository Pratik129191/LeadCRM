from django import forms
from .models import Activity, ActivityType


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = [
            'activity_type',
            'note',
            'next_follow_up'
        ]

        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'next_follow_up': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_activity_type(self):
        activity_type = self.cleaned_data['activity_type']

        if self.user:
            user = self.user
            if activity_type.organization != user.organization:
                raise forms.ValidationError("Invalid activity type.")

        return activity_type

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['activity_type'].queryset = ActivityType.objects.filter(
                organization=self.user.organization
            )
