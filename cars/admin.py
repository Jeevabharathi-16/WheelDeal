from django.contrib import admin
from .models import Vehicle, Cart, SellExchange, LoanRequest

admin.site.register(Vehicle)
admin.site.register(Cart)
admin.site.register(SellExchange)
admin.site.register(LoanRequest)
