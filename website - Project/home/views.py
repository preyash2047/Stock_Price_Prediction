from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

#from django.contrib.auth.forms import


# Create your views here.
def home(request):
    return render(request, "home/home.html")

def signup(request):
    if request.method == "GET":
        return render(request,"home/signup.html", {"form":UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"], password = request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("home")
            except IntegrityError:
                return render(request, "home/signup.html", {"form": UserCreationForm(),
                                                                "error": "Username is taken, Chose new one."})
        else:
            return render(request, "home/signup.html", {"form": UserCreationForm(),
                          "error": "Password did not match"})


def userlogin(request):
    if request.method == "GET":
        return render(request, "home/userlogin.html", {"form":AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user == None:
            return render(request, "home/userlogin.html", {"form": AuthenticationForm(), "error": "Username or Password is incorrect."})
        else:
            login(request, user)
            return redirect("home")

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

def watchlist(request):
    return render(request, "home/watchlist.html",
                  {"error": "Watchlist pending"})


def holdings(request):
    return render(request, "home/holdings.html",
                  {"error": "holdings pending"})

def predictions(request):
    return render(request, "home/predictions.html",
                  {"error": "predictions pending"})

def funds(request):
    return render(request, "home/funds.html",
                  {"error": "funds pending"})