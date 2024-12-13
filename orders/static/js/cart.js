document.addEventListener("DOMContentLoaded", function () {

    // Функция для добавления товара в корзину
    function addToCart(productId) {
        fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.csrfToken,  // Используем переданный CSRF токен
            }
        })
        .then(response => {
            if (response.ok) {
                updateCart();  // Обновляем корзину после добавления товара
            } else {
                console.log('Ошибка при добавлении товара');
            }
        });
    }

    // Функция для удаления товара из корзины
    function removeFromCart(productId) {
        fetch(`/cart/remove/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.csrfToken,  // Используем переданный CSRF токен
            }
        })
        .then(response => {
            if (response.ok) {
                updateCart();  // Обновляем корзину после удаления товара
            } else {
                console.log('Ошибка при удалении товара');
            }
        });
    }

    // Функция для обновления корзины
    function updateCart() {
        fetch('/cart/')
            .then(response => response.json())
            .then(data => {
                const cartList = document.getElementById('cart-list');
                cartList.innerHTML = '';  // Очищаем текущий список товаров в корзине

                data.cart_items.forEach(item => {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.id = `cart-item-${item.id}`;
                    li.innerHTML = `
                        <strong>${item.track_code}</strong> - ${item.status}
                        <br>Вес: ${item.weight} кг
                        <button class="btn btn-danger btn-sm float-end remove-from-cart"
                                data-product-id="${item.id}">Удалить</button>
                    `;
                    cartList.appendChild(li);
                });

                // Обновляем итоговую стоимость и вес
                document.getElementById('total-price').textContent = `Итоговая стоимость: ${data.total_price} сом`;
                document.getElementById('total-weight').textContent = `Общий вес: ${data.total_weight} кг`;
            });
    }

    // Вешаем обработчики на кнопки "Добавить в корзину"
    const addButtons = document.querySelectorAll('.add-to-cart');
    addButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);  // Добавляем товар в корзину
        });
    });

    // Вешаем обработчики на кнопки "Удалить из корзины"
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            removeFromCart(productId);  // Удаляем товар из корзины
        });
    });
});
