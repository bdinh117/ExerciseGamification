from django import forms
from django.contrib.auth.models import User
from .models import Profile, Goal

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class GoalUpdateForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title','text']

