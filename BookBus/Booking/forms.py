from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    aadhar = forms.IntegerField(required=True)
    profile_picture = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'date_of_birth', 'aadhar', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
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
