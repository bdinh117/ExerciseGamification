from django.contrib import admin
from .models import Profile, Goal,AerobicExercise,StrengthExercise,FlexibilityExercise
# Register your models here.

admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(AerobicExercise)
admin.site.register(StrengthExercise)
admin.site.register(FlexibilityExercise)
