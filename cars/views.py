from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Vehicle, SellExchange, LoanRequest


# ---------- HOME ----------
def home(request):
    context = {
        'new_vehicles': Vehicle.objects.filter(condition='new'),
        'old_vehicles': Vehicle.objects.filter(condition='old'),
    }
    return render(request, 'home.html', context)


# ---------- ADD TO CART ----------
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    return redirect('cart')


# ---------- CART ----------
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

    return render(request, 'cart.html', {'items': items, 'total': total})


def remove_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


def increase(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


# ---------- SELL ----------
def sell_exchange(request):
    if request.method == 'POST':
        SellExchange.objects.create(
            user=request.user,
            vehicle_type=request.POST['type'],
            brand=request.POST['brand'],
            model=request.POST['model'],
            year=request.POST['year'],
            description=request.POST['description'],
            price=request.POST['price'],
            exchange=True if 'exchange' in request.POST else False
        )
        return redirect('home')

    return render(request, 'sell.html')


# ---------- LOAN LIST (⭐ THIS WAS MISSING ⭐) ----------
def loan_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'loan_list.html', {'vehicles': vehicles})


# ---------- LOAN ----------
def loan(request, id):
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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')
