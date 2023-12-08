from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, tweet
from django.contrib import messages
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        tweets = tweet.objects.all().order_by("-created_at")
        
    return render(request, 'index.html', {'profile': profile, "tweets": tweets})


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
        my_tweets = tweet.objects.filter(user_id = pk).order_by("-created_at")
        #  Post form logic
        if request.method == "POST":
            current_user_profile = request.user.profile
        # Get form data
            action = request.POST['follow']
        # Decide to follow or Unfollowed
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
                
        return render(request, 'profile_page.html', {'profile': profile, 'my_tweets': my_tweets})
    else:
        messages.success(request, "You mnust be login to vie this page")
        return redirect('index')    