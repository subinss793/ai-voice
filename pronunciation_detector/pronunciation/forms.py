from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'input-field'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username', 'class': 'input-field'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password', 'class': 'input-field'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'input-field'})
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your age', 'class': 'input-field'})
    )
    gender = forms.ChoiceField(
    choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
    widget=forms.Select(attrs={'class': 'input-field'})
    )

    class Meta:
        model = User  # Use your custom User model
        fields = ['username', 'email', 'password1', 'password2', 'age', 'gender']
