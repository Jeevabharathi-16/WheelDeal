# from django.shortcuts import render, redirect
# from .models import *
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User

# def home(request):
#     old = Vehicle.objects.filter(condition='old')
#     new = Vehicle.objects.filter(condition='new')
#     return render(request,'home.html',{'old':old,'new':new})


# def add_to_cart(request,id):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     v = Vehicle.objects.get(id=id)
#     Cart.objects.create(user=request.user, vehicle=v)
#     return redirect('cart')


# def cart(request):
#     c = Cart.objects.filter(user=request.user)
#     return render(request,'cart.html',{'cart':c})


# def sell_exchange(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     if request.method=='POST':
#         SellExchange.objects.create(
#             user=request.user,
#             vehicle_type=request.POST['type'],
#             model=request.POST['model'],
#             year=request.POST['year'],
#             price=request.POST['price'],
#             exchange=True if 'exchange' in request.POST else False
#         )
#         return redirect('home')
#     return render(request,'sell.html')


# def loan(request,id):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     v = Vehicle.objects.get(id=id)
#     if request.method=='POST':
#         LoanRequest.objects.create(
#             user=request.user,
#             vehicle=v,
#             amount=request.POST['amount'],
#             tenure=request.POST['tenure'],
#             contact=request.POST['contact']
#         )
#         return redirect('home')
#     return render(request,'loan.html',{'v':v})


# # ---------- AUTH ----------

# def signup(request):
#     if request.method=='POST':
#         User.objects.create_user(
#             username=request.POST['username'],
#             password=request.POST['password']
#         )
#         return redirect('login')
#     return render(request,'signup.html')


# def user_login(request):
#     if request.method=='POST':
#         u = authenticate(
#             username=request.POST['username'],
#             password=request.POST['password']
#         )
#         if u:
#             login(request,u)
#             return redirect('home')
#     return render(request,'login.html')


# def user_logout(request):
#     logout(request)
#     return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *


# ---------- HOME ----------
def home(request):
    new = Vehicle.objects.filter(condition='new')
    old = Vehicle.objects.filter(condition='old')
    return render(request, 'home.html', {'new': new, 'old': old})


# ---------- SESSION CART ----------
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for vid, qty in cart.items():
        v = Vehicle.objects.get(id=vid)
        subtotal = v.price * qty
        total += subtotal

        items.append({
            'vehicle': v,
            'quantity': qty,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


def remove_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')


# ---------- SELL / EXCHANGE ----------
def sell_exchange(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        SellExchange.objects.create(
            user=request.user,
            vehicle_type=request.POST['type'],
            model=request.POST['model'],
            year=request.POST['year'],
            price=request.POST['price'],
            exchange=True if 'exchange' in request.POST else False
        )
        return redirect('home')

    return render(request, 'sell.html')


# ---------- LOAN ----------
def loan(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    v = Vehicle.objects.get(id=id)

    if request.method == 'POST':
        LoanRequest.objects.create(
            user=request.user,
            vehicle=v,
            amount=request.POST['amount'],
            tenure=request.POST['tenure'],
            contact=request.POST['contact']
        )
        return redirect('home')

    return render(request, 'loan.html', {'v': v})


# ---------- AUTH ----------
def signup(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)

            # OPTIONAL: sync session cart to DB
            session_cart = request.session.get('cart', {})
            for vid, qty in session_cart.items():
                v = Vehicle.objects.get(id=vid)
                c = Cart.objects.filter(user=user, vehicle=v).first()
                if c:
                    c.quantity += qty
                    c.save()
                else:
                    Cart.objects.create(user=user, vehicle=v, quantity=qty)

            request.session['cart'] = {}
            return redirect('home')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def increase_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] += 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')
