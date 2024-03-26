from django import forms
from main.models import Author
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ("fullname", "bio", "profile_pic")

class UpdateImageForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ("profile_pic",)


class CustomAuthForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email", "password",)
        


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Например: NikpupAysav5%'}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Например: NikpupAysav5%'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Вася Пупкин'}),
            'email': forms.EmailInput(attrs={'placeholder': 'VasyaPupkin@mail.ru'}),
        }