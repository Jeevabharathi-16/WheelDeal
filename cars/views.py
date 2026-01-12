from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    old = Vehicle.objects.filter(condition='old')
    new = Vehicle.objects.filter(condition='new')
    return render(request,'home.html',{'old':old,'new':new})


def add_to_cart(request,id):
    if not request.user.is_authenticated:
        return redirect('login')

    v = Vehicle.objects.get(id=id)
    Cart.objects.create(user=request.user, vehicle=v)
    return redirect('cart')


def cart(request):
    c = Cart.objects.filter(user=request.user)
    return render(request,'cart.html',{'cart':c})


def sell_exchange(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method=='POST':
        SellExchange.objects.create(
            user=request.user,
            vehicle_type=request.POST['type'],
            model=request.POST['model'],
            year=request.POST['year'],
            price=request.POST['price'],
            exchange=True if 'exchange' in request.POST else False
        )
        return redirect('home')
    return render(request,'sell.html')


def loan(request,id):
    if not request.user.is_authenticated:
        return redirect('login')

    v = Vehicle.objects.get(id=id)
    if request.method=='POST':
        LoanRequest.objects.create(
            user=request.user,
            vehicle=v,
            amount=request.POST['amount'],
            tenure=request.POST['tenure'],
            contact=request.POST['contact']
        )
        return redirect('home')
    return render(request,'loan.html',{'v':v})


# ---------- AUTH ----------

def signup(request):
    if request.method=='POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request,'signup.html')


def user_login(request):
    if request.method=='POST':
        u = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if u:
            login(request,u)
            return redirect('home')
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
