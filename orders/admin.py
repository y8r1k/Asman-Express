from django.contrib import admin
from .models import Product, Expense, Cart, CartItem, Issuance, IssuedProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('track_code', 'weight', 'client', 'status')
    list_filter = ('status', 'client')
    search_fields = ('track_code',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('manager', 'amount', 'date_time')
    list_filter = ('date_time',)
    search_fields = ('manager__username',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('manager', 'total_weight', 'total_price')
    search_fields = ('manager__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')
    search_fields = ('cart__manager__username', 'product__track_code')

@admin.register(Issuance)
class IssuanceAdmin(admin.ModelAdmin):
    list_display = ('manager', 'total_weight', 'total_price', 'method_of_payment', 'date')
    list_filter = ('method_of_payment', 'date')
    search_fields = ('manager__username',)

@admin.register(IssuedProduct)
class IssuedProductAdmin(admin.ModelAdmin):
    list_display = ('issuance', 'product')
    search_fields = ('issuance__manager__username', 'product__track_code')
