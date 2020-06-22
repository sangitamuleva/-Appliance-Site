from django.shortcuts import render
from .forms import CreateUser
# Create your views here.

def loginPage(request):
    form =CreateUser()
    context={}
    return render(request,'User_Auth/user_login.html',context)


def registerPage(request):
    context = {}
    return render(request, 'User_Auth/user_registration.html', context)

def productPage(request):
    context = {}
    return render(request, 'Accounts/products.html', context)

def homePage(request):
    context = {}
    return render(request, 'Accounts/dashboard.html', context)

def customerPage(request):
    context = {}
    return render(request, 'Accounts/customer.html', context)