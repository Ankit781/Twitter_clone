from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib import messages
# Create your views here.


def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    return render(request, 'index.html', {'profile': profile})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = User.authenticate(username=username, password=password)
        if user is not None:
            return redirect("/") 
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})
    return render(request, "login.html")  


def logoutuser(request):
    logout(request)
    return redirect("login") 

def profile_list(request):
    profiles = Profile.objects.exclude(user = request.user)
    return render(request, 'profile_list.html', {"profiles": profiles})


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        print("Profile information :" ,profile)
        return render(request, 'profile_page.html', {'profile': profile})
    else:
        messages.success(request, "You mnust be login to vie this page")
        return redirect('index')    