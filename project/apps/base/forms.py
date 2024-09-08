from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = ['username', 'email', 'login', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required': True, 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'required': True, 'placeholder': 'Ваша почта'}),
            'login': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'required': True, 'placeholder': 'Ваш логин'}),
        }
