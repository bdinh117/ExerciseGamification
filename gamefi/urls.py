from django.urls import path
from . import views

app_name = 'gamefi'

urlpatterns = [
    path("", views.home, name="home"),
]