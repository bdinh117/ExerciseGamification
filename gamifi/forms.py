from django import forms
from django.contrib.auth.models import User
from .models import Profile, Goal, AerobicExercise, StrengthExercise, FlexibilityExercise

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

class AerobicExerciseForm(forms.ModelForm):
    class Meta:
        model = AerobicExercise
        fields = ['name','duration','duration_suffix','finished']

class StrengthExerciseForm(forms.ModelForm):
    class Meta:
        model = StrengthExercise
        fields = ['name','duration','duration_suffix','finished']

class FlexibilityExerciseForm(forms.ModelForm):
    class Meta:
        model = FlexibilityExercise
        fields = ['name', 'duration', 'duration_suffix','finished']


