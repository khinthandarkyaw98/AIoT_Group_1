from django.db import models

# Create your models here.

class Student(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    
# Create    /   Insert  /   Add - POST
# Retrieve  /   Fetch - GET
# Update    / Edit - PUT
# Delete    / Remove - DELETE