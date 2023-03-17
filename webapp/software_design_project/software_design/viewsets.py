from rest_framework import viewsets
from . import models
from . import serializers

class StudentViewset(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

class StaffViewset(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer


# list(), retrieve(), create(), update(), destroy()
