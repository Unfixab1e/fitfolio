from rest_framework import serializers
from .models import User, ActivityData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ActivityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityData
        fields = ['date', 'steps', 'distance', 'calories_burned', 'user']
