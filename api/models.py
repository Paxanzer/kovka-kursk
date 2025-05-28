from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import random
import string


class User(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('customer', 'Покупатель'),
    )
    
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')
    role = models.CharField(max_length=20, choices=ROLES, default='customer', verbose_name='Роль')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название вида')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', verbose_name='Вид Изделия')
    article = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    specifications = models.TextField(null=True, blank=True, verbose_name='Характеристики')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Основное изображение')
    images = models.ManyToManyField('ProductImage', blank=True, verbose_name='Дополнительные изображения')
    
    def __str__(self):
        return f"{self.name} ({self.article})"

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.alt_text or f"Image {self.id}"
    

def generate_order_code():
    """Генерирует уникальный код заказа"""
    length = 8
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Order.objects.filter(code=code).exists():
            return code

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает получения'),
        ('completed', 'Получен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    code = models.CharField(max_length=8, unique=True, default=generate_order_code)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cancel_reason = models.TextField(blank=True, null=True, verbose_name='Причина отмены')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ {self.code} от {self.user.username}"

    def calculate_total(self):
        """Подсчитывает общую стоимость заказа"""
        total = sum(item.quantity * item.product.price for item in self.items.all())
        self.total_price = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} в заказе {self.order.code}"

    def save(self, *args, **kwargs):
        # Сохраняем цену товара на момент заказа
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        # Пересчитываем общую стоимость заказа
        self.order.calculate_total()

@receiver(pre_delete, sender=Product)
def delete_product_files(sender, instance, **kwargs):
    """Удаляет файлы изображений при удалении продукта"""
    if instance.image:
        instance.image.delete(save=False)
    
    # Удаляем связанные изображения
    for image in instance.images.all():
        image.image.delete(save=False)
        image.delete()

@receiver(pre_delete, sender=ProductImage)
def delete_productimage_files(sender, instance, **kwargs):
    """Удаляет файлы изображений при удалении ProductImage"""
    if instance.image:
        instance.image.delete(save=False)