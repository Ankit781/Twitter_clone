from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, tweet
from django.contrib import messages
from .form import TweetForm, SignUpForm
from django.contrib.auth import backends
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                twt = form.save(commit=False) 
                twt.user = request.user
                twt.save()
                messages.success(request, "You tweet has been posted!")
                return redirect('index')
        tweets = tweet.objects.all().order_by("-created_at")
        return render(request, 'index.html', {'profile': profile, "tweets": tweets, 'form': form})
    return render(request, 'index.html', {'profile': profile})


def loginuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been logged in! Get tweeting!"))
            return redirect("/")  
        else:
            return redirect("loginuser")  
    else:
        return render(request, "login.html")

def logoutuser(request):
    logout(request)
    return redirect("loginuser") 

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, "You must be login to view this page")
        return redirect("/")


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
        messages.success(request, "You must be login to view this page")
        return redirect('index')    
    
    
def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            #  Log in user
            user = authenticate(username = username , password = password1)
            login(request,user)
            messages.success(request, "You have successfully register!")
            return redirect('index')
        else:
            return redirect('register')
    else:
        print("HERE")
        return render(request,"register.html", context= {'form': form})