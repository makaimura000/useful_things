from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from slugify import slugify

User = get_user_model()


class Product(models.Model):
    name = models.CharField('Название', max_length=100)
    value = models.IntegerField('Стоимость')
    old_value = models.IntegerField('Прежняя стоимость', blank=True, null=True)
    discount = models.IntegerField('Скидка', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    image = models.ImageField(
        'Изображение',
        upload_to='product_images/',
        blank=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.old_value:
            if self.old_value > self.value:
                self.discount = (self.old_value - self.value) / self.old_value * 100
            else:
                self.discount = None
        super(Product, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.CharField(max_length=100)
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Order(models.Model):
    created = models.DateTimeField('Создан', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(
        'Изменён',
        auto_now_add=False,
        auto_now=True
    )
    customer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Клиент')
    value = models.IntegerField('Стоимость заказа', default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.pk}'


class Container(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField('Количество', default=1)
    current_product_value = models.IntegerField('Текущая стоимость товара', default=1)
    total_value = models.IntegerField('Стоимость контейнера', default=1)

    class Meta:
        verbose_name = 'Контейнер заказа'
        verbose_name_plural = 'Контейнеры заказа'

    def save(self, *args, **kwargs):
        if Container.objects.filter(
            order=self.order,
            product=self.product
        ).exists():
            same_container = Container.objects.get(
                order=self.order,
                product=self.product
            )
            if same_container != self:
                same_container.delete()
                self.quantity = self.quantity + same_container.quantity
        current_product_value = self.product.value
        self.current_product_value = current_product_value
        self.total_value = self.current_product_value * self.quantity
        super(Container, self).save(*args, **kwargs)


def container_post_signal(sender, instance, **kwargs):
    order = instance.order
    containers_in_order = Container.objects.filter(order=order)
    order_value = 0
    for container in containers_in_order:
        order_value += container.total_value
    order.value = order_value
    order.save()


post_save.connect(container_post_signal, sender=Container)
post_delete.connect(container_post_signal, sender=Container)


class CartContainer(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField('Количество', default=1)
    session_key = models.CharField('Ключ сессии', max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField('Создан', auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Контейнер корзины'
        verbose_name_plural = 'Контейнеры корзины'

    def save(self, *args, **kwargs):
        if CartContainer.objects.filter(
            session_key=self.session_key,
            product=self.product
        ).exists():
            same_cart_container = CartContainer.objects.get(
                session_key=self.session_key,
                product=self.product
            )
            if same_cart_container != self:
                same_cart_container.delete()
        super(CartContainer, self).save(*args, **kwargs)
