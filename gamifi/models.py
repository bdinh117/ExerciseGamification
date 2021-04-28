from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import requests

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User,related_name='friends',blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')

class Comment(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

class Exercise(models.Model):
    url = "https://wger.de/api/v2/exerciseinfo/"
    url2 = "https://wger.de/api/v2/exercisecategory/" #endpoint for the exercise categories
    PARAMS = {'language': '2', 'limit': '300'} #2 = English
    headers = {'Accept': 'application/json', 'Authorization': 'Token ***REMOVED***'}
    response = requests.get(url=url, headers=headers, params=PARAMS)
    response2 = requests.get(url=url2, headers=headers)
    exercises = response.json()["results"]
    categories=response2.json()["results"]
    NAME_CHOICES = [
                ('Running', 'RUNNING'),
                ('Swimming', 'SWIMMING'),
                ('Biking', 'BIKING'),
                ('Walking', 'WALKING')
            ]
    SUFFIX_CHOICES = [
            ('Repetitions', 'repetitions'),
            ('Minutes', 'minutes'),
            ('Hours', 'hours'),
            ('Laps', 'laps')
        ]
    CATEGORY_CHOICES = []
    for e in exercises:
        NAME_CHOICES.append((e["name"],e["name"]))
    for c in categories:
        CATEGORY_CHOICES.append((c['name'],c['name']))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    duration = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES)
    name = models.CharField(max_length=50, choices=NAME_CHOICES)
    exp = models.IntegerField(default=100)
    duration_suffix = models.CharField(max_length=50, choices=SUFFIX_CHOICES)

    def get_absolute_url(self):
        return reverse('gamifi:activity-log')

class ExerciseChoice(models.Model):
    name = models.CharField(max_length=100, blank = True, null = True)
    description=models.TextField(blank = True, null = True)
    image_url=models.CharField(max_length=100,blank = True, null = True)
    category=models.CharField(max_length=20,blank = True, null = True)


# class AerobicExercise(Exercise):
#     NAME_CHOICES = [
#         ('Running', 'RUNNING'),
#         ('Swimming', 'SWIMMING'),
#         ('Biking', 'BIKING'),
#         ('Walking', 'WALKING')
#     ]
#     SUFFIX_CHOICES = [
#         ('Repetitions', 'repetitions'),
#         ('Minutes', 'minutes'),
#         ('Hours', 'hours'),
#         ('Laps', 'laps')
#     ]
#     name = models.CharField(max_length=50, choices=NAME_CHOICES)
#     exp = models.IntegerField(default=100)
#     duration_suffix = models.CharField(max_length=50,choices =SUFFIX_CHOICES)
#
#     @property
#     def type(self):
#         "Returns the exercise type(aerobic)."
#         return 'Aerobic'
#
# class StrengthExercise(Exercise):
#     NAME_CHOICES = [
#         ('Push-Ups', 'PUSH-UPS'),
#         ('Deadlift', 'DEADLIFT'),
#         ('Pull-ups', 'PULL-UPS')
#     ]
#
#     SUFFIX_CHOICES = [
#         ('Repetitions', 'repetitions'),
#         ('Sets', 'sets'),
#         ('Minutes', 'minutes')
#     ]
#     name = models.CharField(max_length=50, choices=NAME_CHOICES)
#     exp = models.IntegerField(default=217)
#     duration_suffix = models.CharField(max_length=50,choices =SUFFIX_CHOICES)
#
#     @property
#     def type(self):
#         "Returns the exercise type(aerobic)."
#         return 'Strength'
#
# class FlexibilityExercise(Exercise):
#     NAME_CHOICES = [
#         ('Lunges', 'LUNGES'),
#         ('Butterfly Stretch', 'BUTTERFLY STRETCH'),
#         ('Yoga', 'YOGA')
#     ]
#     SUFFIX_CHOICES = [
#         ('Repetitions', 'repetitions'),
#         ('Sets', 'sets'),
#         ('Minutes', 'minutes')
#     ]
#     name = models.CharField(max_length=50, choices=NAME_CHOICES)
#     exp = models.IntegerField(default=50)
#     duration_suffix = models.CharField(max_length=50,choices =SUFFIX_CHOICES)
#
#     @property
#     def type(self):
#         "Returns the exercise type(aerobic)."
#         return 'Flexibility'


