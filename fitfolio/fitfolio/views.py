from rest_framework import viewsets
from .models import User, ActivityData
from .serializers import UserSerializer, ActivityDataSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ActivityDataViewSet(viewsets.ModelViewSet):
    queryset = ActivityData.objects.all()
    serializer_class = ActivityDataSerializer