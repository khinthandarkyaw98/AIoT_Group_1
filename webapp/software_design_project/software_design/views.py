from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse


from . models import Student
from . serializers import StudentSerializer

def loginPage(request):
    if request.method=='POST':
        stu_id=request.POST.get('student_id')
        pass1=request.POST.get('password')
       # user=authenticate(request,student_id=stu,student_passport=pass1)

        students = Student.objects.all().values()
        context = {'students': students}
        
        for stu in student:
            if stu['student_id'] == stu_id and stu['student_passport'] == pass1:
                return render(request, 'home.html', context)
            else:
                print('Failed')
    return render (request,'home.html')

def homePage(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'home.html', context)
   

def logoutPage(request):
    return redner(request, 'logout.html')

def studentApi(request):
    if request.method =='GET':
        student = Student.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        return JsonResponse(student_serializer.data, safe=False)
  

# Create your views here.
