from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            "content": forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            )
        }


