from django.contrib import admin
from .models import Product, Expense, Cart, CartItem, Issuance, IssuedProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ('track_code', 'weight', 'client', 'status')
    list_filter = ('status', 'client')
    search_fields = ('track_code', 'client__username')
    list_editable = ('status',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('manager', 'amount', 'date_time', 'comment')
    list_filter = ('manager', 'date_time')
    search_fields = ('manager__username', 'comment')

class CartAdmin(admin.ModelAdmin):
    list_display = ('manager',)
    search_fields = ('manager__username',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')
    list_filter = ('cart', 'product')
    search_fields = ('cart__manager__username', 'product__track_code')

class IssuanceAdmin(admin.ModelAdmin):
    list_display = ('manager', 'total_weight', 'total_price', 'method_of_payment', 'date_time')
    list_filter = ('manager', 'method_of_payment', 'date_time')
    search_fields = ('manager__username',)

class IssuedProductAdmin(admin.ModelAdmin):
    list_display = ('issuance', 'product')
    search_fields = ('issuance__manager__username', 'product__track_code')


# Регистрация моделей в админ-панели
admin.site.register(Product, ProductAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Issuance, IssuanceAdmin)
admin.site.register(IssuedProduct, IssuedProductAdmin)
