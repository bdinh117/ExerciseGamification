from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Goal
from .forms import GoalUpdateForm

# Create your tests here.
'''
class testIfProfileIsCreated(TestCase):
    def setUp(self):
        User.objects.create_user(username="Player1",email="example@gmail.com",password="123456")

    def testProfileExists(self):
        user = User.objects.get(username="Player1")
        self.assertEqual(str(user.profile),"Player1 Profile")
'''

class testIfProfileIsDeleted(TestCase):
    def setUp(self):
        User.objects.create_user(username="Player1",email="example@gmail.com",password="123456")

    def testProfileExists(self):
        user = User.objects.get(username="Player1")
        user.delete()
        self.assertTrue(not Profile.objects.all().exists())

class AddGoalFormTest(TestCase):
    def test_title_starting_lowercase(self):
        form = GoalUpdateForm(data={"title": "Goal1","text":"this is a goal"})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(Goal.objects.filter(title="Goal1",text="this is a goal").exists())

