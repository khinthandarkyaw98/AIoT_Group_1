from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from . models import Student
from . serializers import StudentSerializer

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
            print 

    return render (request,'login.html')

def homePage(request):
    return render(request, 'home.html')

def logoutPage(request):
    return redner(request, 'logout.html')

def studentApi(request):
    if request.method =='GET':
        student = Student.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        return JsonResponse(student_serializer.data, safe=False)

# Create your views here.
