from django.test import TestCase
from ..models import User, ActivityData

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.assertIsInstance(user, User)

class ActivityDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_activity_data_creation(self):
        activity_data = ActivityData.objects.create(user=self.user, date='2021-01-01', steps=1000)
        self.assertEqual(activity_data.steps, 1000)