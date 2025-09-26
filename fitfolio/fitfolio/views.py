from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import User, ActivityData, WeightData, SleepData
from .serializers import UserSerializer, ActivityDataSerializer, WeightDataSerializer, SleepDataSerializer

def dashboard(request):
    """Main dashboard view"""
    return render(request, 'dashboard.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ActivityDataViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityDataSerializer

    def get_queryset(self):
        return ActivityData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activity data (last 30 days)"""
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_data = self.get_queryset().filter(date__gte=thirty_days_ago)
        serializer = self.get_serializer(recent_data, many=True)
        return Response(serializer.data)

class WeightDataViewSet(viewsets.ModelViewSet):
    serializer_class = WeightDataSerializer

    def get_queryset(self):
        return WeightData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent weight data (last 90 days)"""
        ninety_days_ago = datetime.now().date() - timedelta(days=90)
        recent_data = self.get_queryset().filter(date__gte=ninety_days_ago)
        serializer = self.get_serializer(recent_data, many=True)
        return Response(serializer.data)

class SleepDataViewSet(viewsets.ModelViewSet):
    serializer_class = SleepDataSerializer

    def get_queryset(self):
        return SleepData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent sleep data (last 30 days)"""
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_data = self.get_queryset().filter(date__gte=thirty_days_ago)
        serializer = self.get_serializer(recent_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get sleep summary statistics"""
        recent_sleep = self.get_queryset().filter(
            date__gte=datetime.now().date() - timedelta(days=30),
            total_sleep_minutes__gt=0
        )
        
        if not recent_sleep.exists():
            return Response({
                'avg_sleep_minutes': 0,
                'avg_sleep_formatted': '0h 0m',
                'total_nights': 0
            })
        
        total_minutes = sum(s.total_sleep_minutes for s in recent_sleep)
        avg_minutes = total_minutes // len(recent_sleep) if recent_sleep else 0
        avg_hours = avg_minutes // 60
        avg_mins = avg_minutes % 60
        
        return Response({
            'avg_sleep_minutes': avg_minutes,
            'avg_sleep_formatted': f'{avg_hours}h {avg_mins}m',
            'total_nights': len(recent_sleep)
        })