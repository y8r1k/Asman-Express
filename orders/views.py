from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Product, Cart, CartItem, Expense
from .forms import SearchForm, ExpenseForm


def home(request):
    # Получаем все товары
    products = Product.objects.all()

    # Обработка формы поиска
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        client_id = search_form.cleaned_data.get('client_id')
        track_code = search_form.cleaned_data.get('track_code')

        if client_id:
            products = products.filter(client_id=client_id)
        elif track_code:
            products = products.filter(track_code__icontains=track_code)

    # Получаем корзину пользователя (если он авторизован)
    cart = Cart.objects.filter(manager=request.user).first() if request.user.is_authenticated else None
    cart_items = cart.items.all() if cart else []

    # Лучше это сделать в шаблоне и вообще item присвоить отдельной переменной,
    # чтобы по 100 раз не обращаться к БД
    # Считаем итоговую стоимость и общий вес товаров в корзине
    total_price = sum(item.product.weight * 100 for item in cart_items)  # Пример расчета
    total_weight = sum(item.product.weight for item in cart_items)

    # Создаём множество из ID товаров в корзине для быстрого поиска
    cart_product_ids = {item.product.id for item in cart_items}

    # Отправляем данные в шаблон
    return render(request, 'home.html', {
        'products': products,
        'search_form': search_form,
        'cart_product_ids': cart_product_ids,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_weight': total_weight,
        'cart': cart,
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_to_cart(request, product_id):
    # Получаем продукт
    product = Product.objects.get(id=product_id)

    # Проверяем, не добавлен ли этот товар в корзину другого менеджера
    if CartItem.objects.filter(product=product).exists():
        # Если товар уже в корзине другого менеджера, возвращаем ошибку или предупреждение
        return redirect('home')  # Вы можете добавить сообщение об ошибке

    # Ищем корзину текущего менеджера
    try:
        cart = Cart.objects.get(manager=request.user)
    except Cart.DoesNotExist:
        # Если корзины нет, создаем новую
        cart = Cart(manager=request.user, total_weight=0, total_price=0)
        cart.save()

    # Добавляем товар в корзину
    CartItem.objects.create(cart=cart, product=product)

    # Обновляем общий вес и цену
    cart.total_weight += product.weight
    cart.total_price += product.weight * 100  # Пример расчета цены
    cart.save()

    return redirect('home')


# views.py
@login_required
def expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.manager = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'home.html', {'expense_form': form})

# @login_required
# def issue_cart(request):
#     cart = Cart.objects.filter(manager=request.user).first()
#     if cart:
#         # Логика для "выдачи" товаров (обновляем статус или что-то другое)
#         for item in cart.items.all():
#             item.product.status = 'issued'
#             item.product.save()
#
#         # Очистка корзины (если нужно)
#         cart.items.clear()
#
#     return redirect('home')
