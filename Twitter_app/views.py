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
def logouuser(request):
    logout(request)
    return redirect("/login") 

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user = EndUser.objects.create_user(
            name=name, email=email, phone=phone, password=password)
        user.save()
        return redirect("/")
    return render(request, "register.html")
    