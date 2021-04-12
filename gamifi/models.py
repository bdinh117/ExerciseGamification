from django.db import models
from django.contrib.auth.models import User

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