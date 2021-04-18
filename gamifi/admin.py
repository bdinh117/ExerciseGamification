from django.contrib import admin
from .models import Profile,AerobicExercise,StrengthExercise,FlexibilityExercise,FriendRequest,Comment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(AerobicExercise)
admin.site.register(StrengthExercise)
admin.site.register(FlexibilityExercise)
admin.site.register(FriendRequest)
