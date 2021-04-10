from django.contrib import admin
from .models import Profile, Goal,Exercise
# Register your models here.

admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(Exercise)
