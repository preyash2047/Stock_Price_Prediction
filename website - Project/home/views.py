from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

#!pip install yfinance
import yfinance as yf
from .forms import DataModelForm
from .models import DataModel


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

def remove_from_watchlist(request, DataModel_pk):
    temp_data = DataModel.objects.filter(user=request.user).get(pk=DataModel_pk)
    if temp_data.qty == 0:
        temp_data.delete()
        message = "Done"
    else:
        message = "error"

    return redirect("watchlist")


def update_stock_price(request):
    stocks = DataModel.objects.filter(user=request.user)
    for stock in stocks:
        stock.price = yf.Ticker(stock.symbol).info['regularMarketPrice']
        stock.save()
    return redirect("watchlist")


def watchlist(request):
    watchlist_stock = DataModel.objects.filter(user=request.user)
    if request.method == "GET":
        return render(request, "home/watchlist.html", {"error": "", "form": "", "watchlist_stock":watchlist_stock})
    else:
        if request.method == "POST":
            try:
                tempVal = yf.Ticker(request.POST["symbol"]).info['regularMarketPrice']
                form = DataModelForm({
                    "qty": 0,
                    "avgCost":0,
                    "symbol": request.POST["symbol"],
                    "price": tempVal,
                    "csrfmiddlewaretoken": request.POST["csrfmiddlewaretoken"]
                })
                newStock = form.save(commit=False)
                newStock.user = request.user
                newStock.save()
            except:
                return render(request, "home/watchlist.html", {"error": "",
                                                               "message":"Stock added to Watchlist",
                                                               "watchlist_stock":watchlist_stock
                                                               })
                return render(request, "home/watchlist.html", {
                    "error": "Invalid Input! Enter Yahoo Finance Code.",
                    "watchlist_stock":watchlist_stock
                })

        else:
            return render(request, "home/watchlist.html", {"error": "",
                                                           "watchlist_stock": watchlist_stock
                                                           })


def transaction(request):
    if request.method == "GET":
        stock = DataModel.objects.filter(user=request.user)
        return render(request, "home/transaction.html", {"stock":stock})
    else:
        stock = DataModel.objects.filter(user=request.user).get(pk=request.POST["id"])
        stock.avgCost = round(((stock.avgCost * stock.qty) + float(request.POST["price"]) * int(request.POST["qty"]) ) / (stock.qty + int(request.POST["qty"]) ),2)
        if request.POST["transaction"] == "buy":
            stock.qty += int(request.POST["qty"])
        else:
            stock.qty -= int(request.POST["qty"])
            if stock.qty < 0:
                return render(request, "home/transaction.html", {
                    "error": "Invalid Stock Quantity"
                })
        stock.save()
        return redirect("holdings")

def holdings(request):
    holding_stock = DataModel.objects.filter(user=request.user, qty__gt=0)
    return render(request, "home/holdings.html", {"error": "", "form": "", "holding_stock": holding_stock})

def predictions(request):
    return render(request, "home/predictions.html", {"error": "predictions pending"})