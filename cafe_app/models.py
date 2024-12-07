from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Drink(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='drinks/', null=True, blank=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='offers/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
class Dish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    def __str__(self):
        return self.name 
class Cheesecake(models.Model):
    name = models.CharField(max_length=255)  # Название чизкейка
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена чизкейка
    description = models.TextField()  # Описание чизкейка
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.name
# Логирование действий пользователей
class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    action = models.CharField(max_length=255, verbose_name="Действие")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время действия")

    def __str__(self):
        return f"{self.user.username}: {self.action} at {self.timestamp}"

    class Meta:
        verbose_name = "Лог пользователя"
        verbose_name_plural = "Логи пользователей"
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]

# Модель игры
class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    single_player = models.BooleanField(default=True)
    multiplayer = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500)
    trailer_url = models.URLField(max_length=500)

    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Трудный')
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English')
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru')

    def __str__(self):
        return self.title

# Категории и элементы меню
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории", blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100, verbose_name="Название пункта меню")
    description = models.TextField(verbose_name="Описание пункта меню")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активность")

    def __str__(self):
        return self.name

# Профиль пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name="Биография", blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

# Модели стола и заказа
class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    max_seats = models.PositiveIntegerField(verbose_name="Максимальное количество мест")
    reserved = models.BooleanField(default=False, verbose_name="Забронирован")
    reserved_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reserved_tables', verbose_name="Забронировано пользователем"
    )

    def __str__(self):
        return f"Стол {self.number}"

    def clean(self):
        if self.reserved and not self.reserved_by:
            raise ValidationError("Забронированный стол должен быть связан с пользователем.")

    def release(self):
        self.reserved = False
        self.reserved_by = None
        self.save()

    def reserve(self, user):
        if self.reserved:
            raise ValidationError("Стол уже забронирован.")
        self.reserved = True
        self.reserved_by = user
        self.save()

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        indexes = [
            models.Index(fields=['number']),
        ]

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    items = models.ManyToManyField(MenuItem, related_name="orders", verbose_name="Товары")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    in_restaurant = models.BooleanField(default=False, verbose_name="В ресторане")
    table = models.ForeignKey(
        Table, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Стол"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Общая сумма")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    def clean(self):
        if self.in_restaurant and not self.table:
            raise ValidationError("Если заказ в ресторане, необходимо выбрать стол.")
        if not self.items.exists():
            raise ValidationError("Заказ должен содержать хотя бы один товар.")

    def calculate_total_price(self):
        self.total_price = sum(item.price for item in self.items.all())

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)
        if self.in_restaurant and self.table:
            self.table.reserve(self.user)

        # Логирование действий пользователя
        timestamp_str = self.updated_at.isoformat() if isinstance(self.updated_at, timezone.datetime) else str(self.updated_at)
        UserLog.objects.create(
            user=self.user,
            action=f"Создал заказ #{self.id} в статусе {self.status}",
            timestamp=timestamp_str  # Убедитесь, что это строка
        )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        indexes = [
            models.Index(fields=['status']),
        ]

# Тарифы и сессии
class Tariff(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session for {self.user.username}"

# Промоции
class Promotion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

# Модели товаров
class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='items/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    @staticmethod
    def get_active_items():
        return Item.objects.filter(is_active=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=['name']),
        ]

# Компьютеры
class Computer(models.Model):
    name = models.CharField(max_length=100)
    specs = models.TextField()
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return self.name
