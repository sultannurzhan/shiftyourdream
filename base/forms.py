from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label=False,  # Set label to False to remove it
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        label=False,  # Set label to False to remove it
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label=False,  # Set label to False to remove it
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Password confirmation'})
    )






class NoteForm(forms.ModelForm):
    important = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Note
        fields = ['title', 'body', 'important']
        labels = {
            "body": "",
            "title": "",
            "important": "Mark as Important",
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title', '')
        body = cleaned_data.get('body', '')

        # If title and body are empty, mark the title field as not required
        if not title and not body:
            self.fields['title'].required = False

        return cleaned_data