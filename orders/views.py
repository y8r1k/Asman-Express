from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import JsonResponse

from .models import Product, Cart, CartItem, IssuedProduct
from .forms import SearchForm, ExpenseForm, IssuanceForm


def home(request):
    # Получаем все товары с фильтрацией по статусу "не выдан"
    products = Product.objects.filter(status=Product.Status.NOT_ISSUED)

    # Обработка формы поиска
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        search_by = search_form.cleaned_data.get('search_by')
        client_id = search_form.cleaned_data.get('client_id')
        track_code = search_form.cleaned_data.get('track_code')

        if search_by == 'client_id' and client_id:
            # Фильтрация по client_id
            products = products.filter(client_id=client_id)
        elif search_by == 'track_code' and track_code:
            # Фильтрация по track_code
            products = products.filter(track_code__icontains=track_code)

    # Получаем корзину пользователя (если он авторизован)
    cart = Cart.objects.filter(manager=request.user).first() if request.user.is_authenticated else None
    cart_items = cart.items.all() if cart else []

    # Считаем итоговую стоимость и общий вес товаров в корзине
    total_price = sum(item.product.weight * 100 for item in cart_items)  # Пример расчета
    total_weight = sum(item.product.weight for item in cart_items)

    # Создаём множество из ID товаров в корзине для быстрого поиска
    cart_product_ids = {item.product.id for item in cart_items}

    # Рендерим шаблон с переданными данными
    return render(request, 'home.html', {
        'products': products,
        'search_form': search_form,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_weight': total_weight,
        'cart_product_ids': cart_product_ids,
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


# views.py
from django.http import JsonResponse
from .models import Product, Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(manager=request.user)

        # Проверяем, существует ли уже этот товар в корзине
        if not CartItem.objects.filter(cart=cart, product=product).exists():
            CartItem.objects.create(cart=cart, product=product)
        else:
            return JsonResponse({'status': 'error', 'message': 'Товар уже в корзине'})

        return JsonResponse({'status': 'success', 'message': 'Товар добавлен в корзину'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'}, status=400)



@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(manager=request.user).first()
        if cart:
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            if cart_item:
                cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Товар удалён из корзины'})
    return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'}, status=400)


@login_required
def update_cart(request):
    cart = Cart.objects.filter(manager=request.user).first()
    cart_items = cart.items.all() if cart else []

    total_weight = sum(item.product.weight for item in cart_items)
    total_price = sum(item.product.weight * 1000 for item in cart_items)

    return JsonResponse({
        'cart_items': [
            {
                'id': item.product.id,
                'track_code': item.product.track_code,
                'status': item.product.get_status_display(),
                'weight': item.product.weight
            }
            for item in cart_items
        ],
        'total_price': total_price,
        'total_weight': total_weight,
    })


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.manager = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'expense_form.html', {'form': form})


@login_required
def issue_cart(request):
    cart = Cart.objects.filter(manager=request.user).first()

    if not cart:
        return redirect('home')

    # Получаем товары лежащие в корзине
    cart_items = CartItem.objects.filter(cart=cart)

    # Если корзина пуста
    if not cart_items:
        return redirect('home')

    total_weight = sum(item.product.weight for item in cart_items)
    total_price = sum(item.product.weight * 1000 for item in cart_items)

    if request.method == 'POST':
        form = IssuanceForm(request.POST)
        if form.is_valid():
            # Сохраняем новую выдачу
            issuance = form.save(commit=False)
            issuance.manager = request.user
            issuance.total_price = total_price
            issuance.total_weight = total_weight  # Добавляем общий вес
            issuance.save()

            # Создаем записи для каждого товара в корзине
            for item in cart_items:
                IssuedProduct.objects.create(issuance=issuance, product=item.product)
                # Обновляем статус товара на "Выдано"
                item.product.status = Product.Status.ISSUED
                item.product.save()

            # Очищаем корзину
            cart_items.delete()

            return redirect('home')  # После оформления редирект на главную страницу
    else:
        # Создаем форму
        form = IssuanceForm()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_weight': total_weight,
        'total_price': total_price,
        'form': form,
    })
