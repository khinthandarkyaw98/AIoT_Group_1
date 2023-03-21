from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from . models import Student
from . serializers import StudentSerializer
from django.contrib.auth import authenticate, login

def loginPage(request):
    if request.method == 'POST':
        stu_id = request.POST.get('student_id')
        pass1 = request.POST.get('password')
        student = Student.objects.filter(student_id = stu_id)
        for stu in student:
            if stu.student_passport == pass1:
                context = {'students': student}
                print('Login Success')
                return render(request,'home.html',context)
            else:
                print('Login Failed')
                return HttpResponse('Incorrect student id or password')
    return render(request, 'login.html')

@login_required(login_url=settings.LOGIN_URL)
def homePage(request):
    student_id = request.student.student_id
    students = Student.objects.filter(student_id=student_id)
    context = {'students': students}
    return render(request, 'home.html', context)

def logoutPage(request):
    return render(request, 'logout.html')

def studentApi(request):
    if request.method =='GET':
        student = Student.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        return JsonResponse(student_serializer.data, safe=False)

# Create your views here.
