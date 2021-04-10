from django import forms
from django.contrib.auth.models import User
from .models import Profile, Goal, Exercise

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

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['category','name','duration','finished']

    # def __init__(self, *args, **kwargs):
    #     super(ExerciseForm, self).__init__(*args, **kwargs)
    #
    #     if self.instance and self.instance.category is 'Cardio':
    #         new_choices = list(self.fields['name'].choices)
    #         new_choices = [e for e in new_choices if e not in ('Running', 'Swimming')]
    #         self.fields['name'].choices = new_choices
    #         self.fields['name'].widget.choices = new_choices