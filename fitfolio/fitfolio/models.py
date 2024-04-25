from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_set_%(app_label)s_%(class)s",
        related_query_name="user_%(app_label)s_%(class)s",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set_%(app_label)s_%(class)s",
        related_query_name="user_%(app_label)s_%(class)s",
    )

class ActivityData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)  # distance in kilometers
    calories_burned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date}"