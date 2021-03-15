from django.urls import path
from . import views

app_name = 'gamifi'

urlpatterns = [
    path("", views.home, name="home"),
]