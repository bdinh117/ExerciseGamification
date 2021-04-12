from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    friends = models.ManyToManyField(User,related_name='friends', blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'

class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)


class Goal(models.Model):
    title = models.CharField(max_length = 100)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.text