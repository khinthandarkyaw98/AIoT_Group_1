# api <-> mobile app/ web app / etc. json

from rest_framework import serializers
from .models import Student, Mac_point
from .models import Staff

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('__all__')

class Mac_point(serializers.ModelSerializer):
    class Meta:
        model = Mac_point
        fields = ('__all__')

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('__all__')
