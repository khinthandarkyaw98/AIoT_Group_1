from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from . models import Student, Mac_point
from . serializers import StudentSerializer
from django.contrib.auth import authenticate, login
from . broker import run
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import messages

# Function to handle the login page.
def loginPage(request):
    if request.method == 'POST':
        stu_id = request.POST.get('student_id')
        pass1 = request.POST.get('password')
        student = Student.objects.filter(student_id=stu_id)
        mac_info = Mac_point.objects.all()

        # Update student points if new MAC address is detected.
        for mac_obj in mac_info:
            new_mac_address = mac_obj.new_mac_address  # replace with the correct field name
            new_point = mac_obj.new_point  # replace with the correct field name

            for stu in student:
                if new_mac_address == stu.student_mac_address:  # replace with the correct field name
                    stu.student_point += new_point  # replace with the correct field name
                    stu.save()  # save the updated student object
                    mac_obj.delete()  # delete the Mac_point instance

        # Authenticate student login.            
        for stu in student:
            if stu.student_passport == pass1:
                context = {'students': student}
                print('Login Success')
                return render(request, 'home.html', context)

            else:
                print('Login Failed')
                messages.error(request, 'Incorrect student id or password')
                return redirect('login.html')
    return render(request, 'login.html')

# Function to handle the home page.
def homePage(request):
    if request.method == 'POST':
        receriver = request.POST.get('receiver_id')
        transfer_point = request.POST.get('transfer_point')

        print(receriver + ' '+ transfer_point)
    return render(request, 'home.html')

def logoutPage(request):
    return render(request, 'logout.html')

def studentApi(request):
    if request.method =='GET':
        student = Student.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        return JsonResponse(student_serializer.data, safe=False)
    
@receiver(post_save, sender=Student)
def retrieve_student_data(sender, instance, created, **kwargs):
    if created:
        # retrieve data from the database for the newly created student
        method = kwargs.get('method', 'POST')
        run(method=method)
        try:
            student_data = Student.objects.get(student_id=instance.student_id)
            # do something with the retrieved data (e.g. print it)
            print(student_data.student_id, student_data.student_mac_address)
        except Student.MultipleObjectsReturned:
            print(f"Multiple Student objects found with student_id: {instance.student_id}")



# Create your views here.
