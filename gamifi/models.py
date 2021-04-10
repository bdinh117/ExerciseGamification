from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Goal(models.Model):
    title = models.CharField(max_length = 100)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.text

class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('Cardio', 'CARDIO'),
        ('Strength Training', 'STRENGTH TRAINING'),
        ('Flexibility Training', 'FLEXIBILITY TRAINING')
    ]
    NAME_CHOICES =[
        ('Running', 'RUNNING'),
        ('Swimming', 'SWIMMING'),
        ('Push-Ups', 'PUSH-UPS'),
        ('Weight Lifting', 'WEIGHT LIFTING'),
        ('Stretches', 'STRETCHES'),
        ('Yoga', 'YOGA')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,choices=NAME_CHOICES)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    finished = models.BooleanField(default=False)
    duration = models.IntegerField()

    def get_absolute_url(self):
        return reverse('gamifi:home')
