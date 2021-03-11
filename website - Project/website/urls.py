"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('logoutuser/', views.logoutuser, name="logoutuser"),

    #nevbar
    path('watchlist/', views.watchlist, name="watchlist"),
    path('holdings/', views.holdings, name="holdings"),
    path('predictions/', views.predictions, name="predictions"),
    path('funds/', views.funds, name="funds"),
    path('update_stock_price/', views.update_stock_price, name="update_stock_price"),
    path('remove_from_watchlist/<int:DataModel_pk>', views.remove_from_watchlist, name="remove_from_watchlist"),
    path('buy/<int:DataModel_pk>', views.buy, name="buy"),
    path('sell/<int:DataModel_pk>', views.sell, name="sell"),
]
