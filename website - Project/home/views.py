from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

#https://rapidapi.com/lattice-data-lattice-data-default/api/stock-market-data?endpoint=apiendpoint_58e7545e-9d80-4184-9169-e7bcf88ee15a
from .forms import DataModelForm
from .models import DataModel
import http.client

#stock-market api

conn = http.client.HTTPSConnection("stock-market-data.p.rapidapi.com")

#preyash2047@gmail.com
headers = {
    'x-rapidapi-key': "845b1ec26fmsh9303f9df5782b02p1f891bjsne57ff9050fbd",
    'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
    }


#parth21041997@gmail.com
headers = {
    'x-rapidapi-key': "9576b21d89msh826c4a75d8b996fp1b1994jsn22f89fede67c",
    'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
    }
def get_stock_price(stock_code):
    try:
        conn.request("GET", "/stock/quote?ticker_symbol=" + str(stock_code), headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = eval(data)
        return data["quote"]["Current Price"]
    except:
        return False

"""
#alpha vantage api
#https://rapidapi.com/alphavantage/api/alpha-vantage/endpoints
#point2104.........
conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9576b21d89msh826c4a75d8b996fp1b1994jsn22f89fede67c",
    'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
    }

def get_stock_price(stock_code):
    try:
        conn.request("GET", "/query?function=GLOBAL_QUOTE&symbol="  + str(stock_code), headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = eval(data)
        return data["Global Quote"]["05. price"]
    except:
        return False
    
"""
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor


def predict_stock_price(start_year, start_month, start_day, code):
    start = datetime.datetime(start_year, start_month, start_day)
    end = datetime.date.today()
    stockData = data.DataReader(code, 'yahoo', start, end)

    def get_rsi(sdata, m, mem):
        neg = 0
        pos = 0
        RS = 0
        RSI = 100

        upcloses = 0
        downcloses = 0

        n = m
        k = m - 1

        for p in range(mem):
            diff = sdata[n, 3] - sdata[k, 3]
            if (diff >= 0):
                upcloses = upcloses + diff
                pos = pos + 1
            else:
                downcloses = downcloses + diff
                neg = neg + 1

            n = n - 1
            k = k - 1

        downcloses = -downcloses
        if (neg == 0):
            return 100
        else:
            RS = (upcloses * neg) / (downcloses * pos)

        RSI = 100 - (100 / (1 + RS))

        return RSI

    def get_mfi(sdata, m, mem):
        neg = 0
        pos = 0
        MFR = 0
        MFI = 100

        pmflow = 0
        nmflow = 0

        n = m
        k = m - 1

        for p in range(mem):

            typ_pricec = (sdata[n, 0] + sdata[n, 1] + sdata[n, 3]) / 3
            typ_pricep = (sdata[k, 0] + sdata[k, 1] + sdata[k, 3]) / 3

            # print(typ_price,sdata[n,0],sdata[n,1],sdata[n,3])

            if (typ_pricec >= typ_pricep):
                pmflow = pmflow + ((sdata[n, 4]) * (typ_pricec))
                pos = pos + 1
            else:
                nmflow = nmflow + ((sdata[n, 4]) * (typ_pricec))
                neg = neg + 1

            n = n - 1
            k = k - 1

        if (neg == 0):
            return 100
        else:
            MFR = pmflow / nmflow

        MFI = 100 - (100 / (1 + MFR))

        return MFI

    def get_ema(sdata, m, mem, EMAp):

        EMA = sdata[m, 3] * (2 / (1 + mem)) + (1 - (2 / (1 + mem))) * EMAp
        # print("EMA",EMA)

        return EMA

    def get_so(sdata, m, mem):

        SO = ((sdata[m, 3] - sdata[m, 1]) / (sdata[m, 0] - sdata[m, 1])) * 100
        # print("SO",SO)
        return SO

    memory = 14
    sdat2 = stockData.reset_index()
    del sdat2["Date"]
    del sdat2["Adj Close"]
    sdat3 = np.array(sdat2, dtype=np.float32)

    # print(sdat3[0])

    df1 = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'RSI', 'MFI', 'EMA', 'SO', 'CloseNext'])

    df2 = pd.DataFrame(columns=['Close', 'RSI', 'MFI', 'EMA', 'SO', 'CloseNext'])

    arr = np.array(df1.values)

    # print("Printing j\n")

    EMAp = 0
    acc = 0

    for i in range(memory):
        acc = acc + sdat3[i, 3]

    EMAp = acc / memory

    # for i in range(len(sdat3) -memory):
    for i in range(len(sdat3) - 1 - memory):
        j = i + memory

        RSI = get_rsi(sdat3, j, memory)
        # print("RSI:",RSI)

        MFI = get_mfi(sdat3, j, memory)
        # print("MFI:",MFI)

        EMA = get_ema(sdat3, j, memory, EMAp)
        EMAp = EMA

        SO = get_so(sdat3, j, memory)

        N_close = sdat3[j + 1, 3]

        rec1 = [sdat3[j, 2], sdat3[j, 0], sdat3[j, 1], sdat3[j, 3], sdat3[j, 4], RSI, MFI, EMA, SO, N_close]
        rec2 = [sdat3[j, 3], RSI, MFI, EMA, SO, N_close]

        if (sdat3[j, 4] != 0):
            d1 = {"Open": sdat3[j, 2], "High": sdat3[j, 0], "Low": sdat3[j, 1], "Close": sdat3[j, 3],
                  "Volume": sdat3[j, 4], "RSI": RSI, "MFI": MFI, "EMA": EMA, "SO": SO, "CloseNext": N_close}
            df1.loc[i] = rec1
            df2.loc[i] = rec2

    # ANN
    dataset = df1
    y = pd.DataFrame(dataset['CloseNext'])
    X = dataset.drop(['CloseNext'], axis=1)

    X = np.array(X)
    y = np.array(y)
    # X = X[1700:2030,:]
    # y = y[1700:2030,:]
    y = y.flatten()

    # Feature scaling
    scaled = StandardScaler()
    scaled.fit(X)
    X = scaled.transform(X)

    # Train Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    ## ANN implementation
    # define base model of our neural network for regression taks
    def endgame():
        # Adding the neurons in various layers
        model = Sequential()
        model.add(Dense(9, input_dim=9, kernel_initializer='normal', activation='relu'))
        model.add(Dense(15, kernel_initializer='normal', activation='relu'))
        model.add(Dense(8, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        # Compile model for our use in KerasRegressor
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mape'])
        return model

    ann_regression = KerasRegressor(build_fn=endgame, epochs=100, batch_size=5, verbose=1)

    ann_regression.fit(X_train, y_train)

    ann_predict = ann_regression.predict(X_test)

    error = mean_absolute_error(ann_predict, y_test)
    per_err = (error / np.mean(y_test)) * 100
    print('The mean absolute error is {} and percentage error is {}.'.format(error, per_err))

    return ann_regression.predict(scaled.transform([df1.iloc[-1, :-1].values.tolist()]))

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

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

@login_required
def remove_from_watchlist(request, DataModel_pk):
    temp_data = DataModel.objects.filter(user=request.user).get(pk=DataModel_pk)
    if temp_data.qty == 0:
        temp_data.delete()
        message = "Done"
    else:
        message = "error"

    return redirect("watchlist")

@login_required
def update_stock_price(request):
    stocks = DataModel.objects.filter(user=request.user)
    for stock in stocks:
        stock.price = get_stock_price(stock)
        stock.save()
    return redirect("watchlist")

@login_required
def watchlist(request):
    watchlist_stock = DataModel.objects.filter(user=request.user)
    if request.method == "GET":
        return render(request, "home/watchlist.html", {"error": "", "form": "", "watchlist_stock":watchlist_stock})
    else:
        if request.method == "POST":
            try:
                print("In try ")
                tempVal = get_stock_price(request.POST["symbol"])
                print(tempVal)
                if tempVal == False:
                    raise Exception("Invalid Stock Code")
                else:
                    form = DataModelForm({
                        "qty": 0,
                        "avgCost": 0,
                        "symbol": request.POST["symbol"],
                        "price": tempVal,
                        "csrfmiddlewaretoken": request.POST["csrfmiddlewaretoken"]
                    })
                    newStock = form.save(commit=False)
                    newStock.user = request.user
                    newStock.save()
                    #updating stock price
                    for stock in watchlist_stock:
                        if stock.symbol == request.POST["symbol"]:
                            stock.price = tempVal
                            stock.save()
                    print("before render")
                    return render(request, "home/watchlist.html", {"error": "",
                                                                   "message": "Stock added to Watchlist",
                                                                   "watchlist_stock": watchlist_stock
                                                                   })
            except:
                return render(request, "home/watchlist.html", {"error": "",
                                                               "message":"Invalid Stock Code!",
                                                               "watchlist_stock":watchlist_stock
                                                               })
        else:
            return render(request, "home/watchlist.html", {"error": "",
                                                           "watchlist_stock": watchlist_stock
                                                           })

@login_required
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

@login_required
def holdings(request):
    holding_stock = DataModel.objects.filter(user=request.user, qty__gt=0)
    return render(request, "home/holdings.html", {"error": "", "form": "", "holding_stock": holding_stock})

@login_required
def predictions(request):
    if request.method == "GET":
        return render(request, "home/predictions.html")
    else:
        # parameter
        start_year = 2011
        start_month = 1
        start_day = 1
        code = request.POST["symbol"]
        try:
            predicted_price = predict_stock_price(start_year, start_month, start_day, code)
            predicted_price = round(float(predicted_price),2)
            message = code + "'s predicted price is " + str(predicted_price) + " for next trading day."
            return render(request, "home/predictions.html", {"error": "", "stock_message": message})
        except :
            message = "You have entered wrong Stock. Enter stock code as per yahoo finance"
            return render(request, "home/predictions.html", {"error": "", "message" : message})