from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Client(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return f'Клиент : {self.id}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Product(models.Model):
    class Status(models.TextChoices):
        ISSUED = ('issued', 'Выдан')
        NOT_ISSUED = ('not_issued', 'Не выдан')

    track_code = models.CharField(verbose_name='Трек-код', max_length=255)
    weight = models.DecimalField(verbose_name='Вес (кг)', max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_ISSUED, verbose_name="Статус")

    def __str__(self):
        return f'{self.track_code} - {self.status}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Expense(models.Model):
    amount = models.DecimalField(verbose_name='Сумма расхода (сом)', max_digits=10, decimal_places=2)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер')
    date_time = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)

    def __str__(self):
        return f'{self.manager.username} - расход'

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'


class Cart(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер')

    def __str__(self):
        return f'Корзина для {self.manager.username}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'Товар: {self.product.track_code}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ('cart', 'product')  # Один товар может быть в корзине только один раз


class Issuance(models.Model):
    # Модель выдачи
    # Корзина ---> Выдача
    # Поля: 1) общий вес
    #       2) общая цена
    #       3) способ оплаты
    #       4) кто выдал
    #       5) комментарий опционально
    #       6) дата выдачи
    class MethodOfPayment(models.TextChoices):
        CASH = ('cash', 'наличка')
        MBank = ('mbank', 'мбанк')
        OPTIMA = ('optima', 'optima')

    total_weight = models.DecimalField(verbose_name='Общий вес (кг)', max_digits=10, decimal_places=2)
    total_price = models.DecimalField(verbose_name='Общая стоимость (сом)', max_digits=10, decimal_places=2)
    method_of_payment = models.CharField(verbose_name='Метод оплаты', max_length=30, choices=MethodOfPayment.choices)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто выдал')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    date_time = models.DateTimeField(verbose_name='Дата и время выдачи', auto_now_add=True)

    def __str__(self):
        return f'Выдача менеджера {self.manager.username}'

    class Meta:
        verbose_name = 'Выдача'
        verbose_name_plural = 'Выдачи'


class IssuedProduct(models.Model):
    # Таблица связывающая выдачи менеджера с товарами
    issuance = models.ForeignKey(Issuance, on_delete=models.CASCADE, verbose_name='Выдача')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'{self.product.track_code} для {self.issuance}'

    class Meta:
        verbose_name = 'Выданный товар'
        verbose_name_plural = 'Выданные товары'
