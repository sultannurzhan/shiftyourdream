from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light border-0 py-2', 'placeholder': 'Enter your username'}),
    )
    password1 = forms.CharField(
        label="Password",  
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light border-0 py-2', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",  
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control  bg-light border-0 py-2', 'placeholder': 'Confirm your password'})
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
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': None,
            'email': None
        }
        labels = {
            "username": "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name"
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
