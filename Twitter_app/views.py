from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, tweet
from django.contrib import messages
from .form import TweetForm, SignUpForm, ProfilePicForm
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
        profiles = Profile.objects.all() 
        return render(request, 'index.html', {'profiles': profiles, "tweets": tweets, 'form': form})
    return render(request, 'index.html', {})


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
                
        return render(request, 'profile_page.html', {'profile': profile, 'my_tweets': my_tweets })
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
            messages.success(request, (str(form.errors) + "Something went wrong"))
            return redirect('register')
    else:
        return render(request,"register.html", context= {'form': form})
    
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        profile_user = Profile.objects.get(user__id = request.user.id)
        
        user_form = SignUpForm(request.POST or None,request.FILES or None, instance = current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None, instance = profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Your profile has been updated!")
            return redirect('/')
        else: 
            print(user_form.errors)  
            return render(request,"update_user.html", {'user_form': user_form,'profile_form': profile_form})
    else:
        messages.success(request, "You Must Be Logged In To Update Your Profile!")
        return redirect('/')
    
def tweet_likes(request, pk):
    if request.user.is_authenticated:
        tweets = get_object_or_404(tweet, id=pk)
        if tweets.likes.filter(id = request.user.id):
            tweets.likes.remove(request.user)
        else:
            tweets.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "You Must Be Logged In To Update Your Profile!")
        return redirect('/')
    
def tweet_show(request, pk):
    if request.user.is_authenticated:
        twt = get_object_or_404(tweet, id=pk)
        profiles = Profile.objects.filter(id = twt.user.id)
        if twt:
            return render(request, "show_tweet.html", {"tweet":twt, 'profiles': profiles})
        else:
            messages.success(request, "This Tweet does not exist!")
            return redirect('/')
        
        
def unfollow(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        request.user.profile.follows.remove(profile)
        
        request.user.profile.save()
        
        messages.success(request, f"YouHave Successfully Unfollowed {profile.user.username}.")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "You Must Be Logged In To Update Your Profile!")
        return redirect('/')

def follow(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        request.user.profile.follows.add(profile)
        
        request.user.profile.save()
        
        messages.success(request, f"YouHave Successfully followed {profile.user.username}.")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "You Must Be Logged In To Update Your Profile!")
        return redirect('/')
    
def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'followers.html', {"profiles": profiles})
        else:
            messages.success(request, "That's not your profile page. ")
            return redirect("/")
    else:
        messages.success(request, "You must be login to view this page")
        return redirect("/")


def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'follows.html', {"profiles": profiles})
        else:
            messages.success(request, "That's not your profile page. ")
            return redirect("/")
    else:
        messages.success(request, "You must be login to view this page")
        return redirect("/")
    
    
def delete_tweet(request,pk):
    if request.user.is_authenticated:
        twt = get_object_or_404(tweet, id=pk)
        if request.user.username == twt.user.username:
            twt.delete()
            messages.success(request, "The tweet has been deleted.")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Not your tweet")
            return redirect("/")
    else:
        messages.success(request, "You must be login to delete this tweet!")
        return redirect(request.META.get('HTTP_REFERER'))
 
    
def edit_tweet(request,pk):
    if request.user.is_authenticated:
        twt = get_object_or_404(tweet, id=pk)
        if request.user.username == twt.user.username:
            form = TweetForm(request.POST or None, instance = twt)
            if request.method == "POST":
                if form.is_valid():
                    twt = form.save(commit=False) 
                    twt.user = request.user
                    twt.save()
                    messages.success(request, "You tweet has been Updated !")
                    return redirect('index')
            else:
                return render(request,"edit_tweet.html", {'form': form,"tweet":twt})
        else:
            messages.success(request, "Not your tweet")
            return redirect("/")        
    else:
        messages.success(request, "You must be login to edit this tweet!")
        return redirect(request.META.get('HTTP_REFERER'))
    
    
def search(request):
    if request.method == "POST":
        search = request.POST["search"]
        #  Search for tweet
        searched = tweet.objects.filter(body__contains = search)
        profiles = Profile.objects.all() 
        return render(request, "search.html", {"search":search, "searched":searched, "profiles":profiles})
    else:
        return render(request, "search.html", {})
    