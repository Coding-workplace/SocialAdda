from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
# Create your views here.


def home_view(request):
    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    return render(request, "feed.html", {
        "posts": posts,
        "suggestions": suggestions,
        "page": "all_posts",
        'profile': False
    })


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
				return redirect("home")
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
				return redirect("home")
			else:
				messages.error(request,"Invalid Credentials!")
				return redirect("/")
	else:
		return render(request,"login.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return redirect("/")
