from django.contrib import admin
from .models import Profile, FriendRequest,Comment, ExerciseChoice, Exercise
# Register your models here.


admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(ExerciseChoice)
admin.site.register(Exercise)
admin.site.register(FriendRequest)
