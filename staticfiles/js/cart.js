document.addEventListener("DOMContentLoaded", function () {

    // Обновление корзины
    function updateCart() {
        fetch("/cart/")
            .then(response => response.text())
            .then(html => {
                const cartContainer = document.getElementById("cart-container");
                cartContainer.innerHTML = html;
                attachEventListeners();
            });
    }

    // Вешаем обработчики событий на кнопки добавления и удаления
    function attachEventListeners() {
        const addToCartButtons = document.querySelectorAll(".add-to-cart");
        const removeFromCartButtons = document.querySelectorAll(".remove-from-cart");

        addToCartButtons.forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.dataset.productId;
                fetch(`/cart/add/${productId}/`, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCSRFToken() }
                }).then(response => {
                    if (response.ok) {
                        updateCart();
                    }
                });
            });
        });

        removeFromCartButtons.forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.dataset.productId;
                fetch(`/cart/remove/${productId}/`, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCSRFToken() }
                }).then(response => {
                    if (response.ok) {
                        updateCart();
                    }
                });
            });
        });
    }

    // Получаем CSRF токен из формы
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    attachEventListeners();
});
