from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    friends = models.ManyToManyField(User,blank=True,related_name='friends')
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_count(self):
        return self.friends.all().count()

STATUS_CHOICES = (('send', 'send'),('accepted','accepted'))
class Relationship(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    reciever = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='reciever')
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.sender}-{self.reciever}-{self.status}'

class Goal(models.Model):
    title = models.CharField(max_length = 100)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.text