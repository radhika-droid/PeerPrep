# notes/forms.py
from django import forms
from .models import StudyNote

class StudyNoteForm(forms.ModelForm):
    class Meta:
        model = StudyNote
        fields = ['title', 'subject', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note title'
            }),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={
                'accept': '.pdf,.doc,.docx,.txt,.png,.jpg,.jpeg'
            })
        }