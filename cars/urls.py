from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('add/<int:id>/', add_to_cart, name='add'),
    path('cart/', cart, name='cart'),
    path('remove/<int:id>/', remove_cart, name='remove'),
    path('increase/<int:id>/', increase, name='increase'),
    path('decrease/<int:id>/', decrease, name='decrease'),

    path('sell/', sell_exchange, name='sell'),
    path('loan/<int:id>/', loan, name='loan'),

    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
