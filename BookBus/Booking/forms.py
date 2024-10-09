from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter your first name',
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter your first name'"
        })
    )

    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter your last name',
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter your last name'"
        })
    )

    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter your username',
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter your username'"
        })
    )

    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter email address', 
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter email address'",
            'pattern': '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{1,63}$'
        })
    )

    phone_number = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter 10-digit phone number', 
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter 10-digit phone number'",
            'pattern': '[0-9]{10}'
        })
    )

    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'common-input form-control', 
            'placeholder': 'Select your date of birth', 
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Select your date of birth'"
        })
    )

    aadhar = forms.IntegerField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter Aadhaar number', 
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter Aadhaar number'",
            'pattern': '[0-9]{12}'
        })
    )

    profile_picture = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'common-input form-control'
        })
    )

    password1 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Enter password', 
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Enter password'"
        })
    )

    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'class': 'common-input form-control', 
            'placeholder': 'Retype password', 
            'onfocus': "this.placeholder = ''", 
            'onblur': "this.placeholder = 'Retype password'"
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone_number', 'date_of_birth', 'aadhar', 'profile_picture']

    # Custom save method
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                aadhar=self.cleaned_data['aadhar'],
                profile_picture=self.cleaned_data.get('profile_picture')
            )
            profile.save()
        return user
