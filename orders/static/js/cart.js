document.addEventListener('DOMContentLoaded', function () {
    // Функция для обновления кнопок в шаблоне home.html
    function updateButtonStates(productId, action) {
        const addButton = document.querySelector(`.add-to-cart[data-product-id="${productId}"]`);
        const removeButton = document.querySelector(`.remove-from-cart[data-product-id="${productId}"]`);

        if (action === 'add') {
            addButton.setAttribute('hidden', true);
            removeButton.removeAttribute('hidden');
        } else {
            addButton.removeAttribute('hidden');
            removeButton.setAttribute('hidden', true);
        }
    }

    // Обработчик для добавления товара в корзину
    document.querySelectorAll('.add-to-cart').forEach(function (button) {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateButtonStates(productId, 'add');
                        updateCart();
                    } else {
                        alert(data.message);
                    }
                });
        });
    });

    // Обработчик для удаления товара из корзины
    document.querySelectorAll('.remove-from-cart').forEach(function (button) {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            fetch(`/cart/remove/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateButtonStates(productId, 'remove');
                        updateCart();
                    } else {
                        alert(data.message);
                    }
                });
        });
    });

    function updateCart() {
        fetch('/cart/')
            .then(response => response.json())
            .then(data => {
                const cartList = document.getElementById('cart-list');
                if (cartList) {
                    cartList.innerHTML = '';  // Очистить старые товары в корзине

                    data.cart_items.forEach(item => {
                        const listItem = document.createElement('li');
                        listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
                        listItem.id = `cart-item-${item.id}`;
                        listItem.innerHTML = `
                                <div><strong>${item.track_code}</strong> - ${item.status}<br><small>Вес: ${item.weight} кг</small></div>
                                <button class="btn btn-danger btn-sm remove-from-cart" data-product-id="${item.id}"><i class="bi bi-trash"></i> Удалить</button>
                            `;
                        cartList.appendChild(listItem);

                        // Добавляем обработчик для кнопки удаления
                        listItem.querySelector('.remove-from-cart').addEventListener('click', function () {
                            const productId = this.getAttribute('data-product-id');
                            fetch(`/cart/remove/${productId}/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': window.csrfToken
                                }
                            })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.status === 'success') {
                                        updateCart();
                                    } else {
                                        alert(data.message);
                                    }
                                });
                        });
                    });

                    document.getElementById('total-price').textContent = `Итоговая стоимость: ${data.total_price} сом`;
                    document.getElementById('total-weight').textContent = `Общий вес: ${data.total_weight} кг`;
                }
            });
    }
});