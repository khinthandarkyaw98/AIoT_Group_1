from django.db import models

# Define your models for the application here.

# Student model representing individual students.
class Student(models.Model):
    student_name = models.CharField(max_length=50) # Name of the student
    student_id = models.IntegerField(unique=True) # Unique student ID
    student_point = models.IntegerField(null=True) # Points accumulated by the student
    student_passport = models.CharField(max_length=10) # Passport information of the student
    student_participation_status = models.CharField(max_length=50) # Student's participation status
    student_mac_address = models.CharField(max_length=50) # MAC address of the student's device


# Mac_point model representing MAC address and associated points.
class Mac_point(models.Model):
    new_mac_address = models.CharField(max_length=50) # MAC address
    new_point = models.IntegerField(null=True) # Points associated with the MAC address

# Trash model representing different types of trash and their points.
class Trash(models.Model):
    trash_type = models.CharField(max_length=50) # Type of trash
    trash_point = models.IntegerField() # Points associated with the trash type

# Student_Trash model representing the trash disposed of by a student.
class Student_Trash(models.Model):
    student_id = models.ForeignKey('software_design.Student', on_delete = models.CASCADE) # Foreign key to Student model
    trash_id = models.ForeignKey('software_design.Trash', Trash) # Foreign key to Trash model
    timestamp = models.DateField() # Date of the trash disposal

class Staff(models.Model):
    staff_name = models.CharField(max_length = 50)
    staff_password = models.CharField(max_length = 50)

class Case_Management(models.Model):
    student_trash_id = models.ForeignKey('software_design.Student_Trash', on_delete = models.CASCADE)
    staff_id = models.ForeignKey('software_design.Staff', on_delete = models.CASCADE)
    action = models.CharField(max_length = 50)

class Reward_History(models.Model):
    reward_amount = models.IntegerField()
    student_id = models.ForeignKey('software_design.Student', on_delete = models.CASCADE)
    date_earned = models.DateField()

class Sender(models.Model):
     student_id = models.ForeignKey('software_design.Student', on_delete = models.CASCADE)
     transfer_point = models.IntegerField()

class Reciever(models.Model):
    student_id = models.ForeignKey('software_design.Student', on_delete = models.CASCADE)
    transfer_point = models.IntegerField()
    sender_if = models.ForeignKey('software_design.Sender', on_delete = models.CASCADE)
    
# Create    /   Insert  /   Add - POST
# Retrieve  /   Fetch - GET
# Update    / Edit - PUT
# Delete    / Remove - DELETE
