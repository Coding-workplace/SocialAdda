from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from .models import *
# Create your views here.

def profile_view(request):
	pass

def signup_view(request):
	pass

def login_view(request):
	'''login'''
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			messages.success(request,"Login Successfully!")
			return redirect("home_page")
		else:
			messages.error(request,"Invalid Credentials!")
	else:
		return HttpResponse("Get request")

def logout_view(request):
    logout(request)
	messages.success(request,"Logout Successfully!")
    return redirect("/")