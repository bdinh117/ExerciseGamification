from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment, Exercise

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title','body']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name','duration','duration_suffix','category','finished']


# class AerobicExerciseForm(forms.ModelForm):
#     class Meta:
#         model = AerobicExercise
#         fields = ['name','duration','duration_suffix','finished']
#
# class StrengthExerciseForm(forms.ModelForm):
#     class Meta:
#         model = StrengthExercise
#         fields = ['name','duration','duration_suffix','finished']
#
# class FlexibilityExerciseForm(forms.ModelForm):
#     class Meta:
#         model = FlexibilityExercise
#         fields = ['name', 'duration', 'duration_suffix','finished']


