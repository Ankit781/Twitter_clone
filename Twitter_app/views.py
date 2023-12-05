from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')


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


def google_logout(request):
    return redirect('https://accounts.google.com/logout')
