from rest_framework import serializers
from .models import User, ActivityData, WeightData, SleepData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']

class ActivityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityData
        fields = ['id', 'date', 'steps', 'distance', 'calories_burned', 'user']
        read_only_fields = ['user']

class WeightDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightData
        fields = ['id', 'date', 'weight', 'created_at', 'user']
        read_only_fields = ['user', 'created_at']

class SleepDataSerializer(serializers.ModelSerializer):
    sleep_duration_formatted = serializers.SerializerMethodField()

    class Meta:
        model = SleepData
        fields = [
            'id', 'date', 'bedtime', 'sleep_start', 'sleep_end', 'wake_time',
            'total_sleep_minutes', 'deep_sleep_minutes', 'light_sleep_minutes',
            'rem_sleep_minutes', 'awake_minutes', 'sleep_quality_score',
            'created_at', 'user', 'sleep_duration_formatted'
        ]
        read_only_fields = ['user', 'created_at']

    def get_sleep_duration_formatted(self, obj):
        """Format sleep duration as 'Xh Ym'"""
        if obj.total_sleep_minutes:
            hours = obj.total_sleep_minutes // 60
            minutes = obj.total_sleep_minutes % 60
            return f"{hours}h {minutes}m"
        return "0h 0m"
