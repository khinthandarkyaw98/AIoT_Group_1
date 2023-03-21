from django.contrib import admin
from .models import Student

class PersonAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'student_point', 'student_passport')

admin.site.register(Student, PersonAdmin)
