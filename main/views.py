from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def profile_view(request):
	pass

def signup_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		fname = request.POST["firstname"]
		lname = request.POST["lastname"]
		profile = request.FILES.get("profile")
		cover = request.FILES.get('cover')
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		checkUser = User.objects.filter(username=username)
		checkEmail = User.objects.filter(email=email)
		if checkUser:
				messages.error(request,"Username already taken!")
				return redirect("/signup")
		elif checkEmail:
				messages.error(request,"Account already exist with this email!")
				return redirect("/signup")
		else:
				user = User.objects.create_user(username, email, password)
				user.first_name = fname
				user.last_name = lname
				if profile is not None:						
						user.profile_pic = profile
				else:
						user.profile_pic = "profile_pic/no_pic.png"
				user.cover = cover           
				user.save()
				Follower.objects.create(user=user)
				login(request, user)
				messages.success(request,"User created")
				return redirect("home_page")
	else:
		return render(request,"signup.html")
def login_view(request):
	'''login'''
	if request.method == 'POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		if username=="" or password == "":
			messages.error(request,"username or password is empty!")
		else:
			user=authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				messages.success(request,"Login Successfully!")
				return redirect("home_page")
			else:
				messages.error(request,"Invalid Credentials!")
				return redirect("/")
	else:
		return render(request,"login.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return redirect("/")
