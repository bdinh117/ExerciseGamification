from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


# Create your tests here.
class testIfProfileIsCreated(TestCase):
    def setUp(self):
        User.objects.create_user(username="Player1",email="example@gmail.com",password="123456")

    def testProfileExists(self):
        user = User.objects.get(username="Player1")
        self.assertEqual(str(user.profile),"Player1 Profile")


class testIfProfileIsDeleted(TestCase):
    def setUp(self):
        User.objects.create_user(username="Player1",email="example@gmail.com",password="123456")

    def testProfileExists(self):
        user = User.objects.get(username="Player1")
        user.delete()
        self.assertTrue(not Profile.objects.all().exists())

