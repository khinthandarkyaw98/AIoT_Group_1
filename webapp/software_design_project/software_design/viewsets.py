from rest_framework import viewsets, permissions, status
from . import models
from . import serializers

class StudentViewset(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.AllowAny]

class Mac_pointViewset(viewsets.ModelViewSet):
    queryset = models.Mac_point.objects.all()
    serializer_class = serializers.Mac_point
    permission_classes = [permissions.AllowAny]

class StaffViewset(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [permissions.AllowAny]


# list(), retrieve(), create(), update(), destroy()
