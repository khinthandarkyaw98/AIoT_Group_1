# api <-> mobile app/ web app / etc. json

from rest_framework import serializers
from .models import Student, Mac_point
from .models import Staff

# Define serializers for the application's data models to facilitate JSON data exchange.
# StudentSerializer for serializing/deserializing Student model data.

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student # Specify the model to be serialized
        fields = ('__all__') # Specify the model to be serialized

        
# Mac_pointSerializer for serializing/deserializing Mac_point model data.
class Mac_point(serializers.ModelSerializer):
    class Meta:
        model = Mac_point # Specify the model to be serialized
        fields = ('__all__') # Serialize all fields of the model

        
# StaffSerializer for serializing/deserializing Staff model data.
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff # Specify the model to be serialized
        fields = ('__all__') # Serialize all fields of the model
