from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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

class UserProfile(models.Model):
    """Extended user profile for health data integration"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    hc_gateway_user_id = models.CharField(max_length=100, blank=True, null=True, 
                                         help_text="HCGateway user ID for health data sync")
    sync_enabled = models.BooleanField(default=False, 
                                      help_text="Enable automatic health data sync")
    last_sync = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class ActivityData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)  # distance in kilometers
    calories_burned = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class WeightData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()  # weight in kg
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg - {self.date}"

class SleepData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # The date for which sleep is being tracked
    bedtime = models.DateTimeField(null=True, blank=True)  # When user went to bed
    sleep_start = models.DateTimeField(null=True, blank=True)  # When user fell asleep
    sleep_end = models.DateTimeField(null=True, blank=True)  # When user woke up
    wake_time = models.DateTimeField(null=True, blank=True)  # When user got out of bed
    total_sleep_minutes = models.IntegerField(default=0)  # Total sleep duration in minutes
    deep_sleep_minutes = models.IntegerField(default=0, null=True, blank=True)
    light_sleep_minutes = models.IntegerField(default=0, null=True, blank=True)
    rem_sleep_minutes = models.IntegerField(default=0, null=True, blank=True)
    awake_minutes = models.IntegerField(default=0, null=True, blank=True)
    sleep_quality_score = models.IntegerField(null=True, blank=True)  # 1-100 score
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        hours = self.total_sleep_minutes // 60
        minutes = self.total_sleep_minutes % 60
        return f"{self.user.username} - {hours}h {minutes}m - {self.date}"