# from django.contrib import admin
# from .models import UserLog, Item, Table, Order, Computer, Tariff
# from django.contrib import admin
# from .models import Promotion

# @admin.register(Promotion)
# class PromotionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'start_date', 'end_date', 'active')
#     list_filter = ('active',)
#     search_fields = ('title', 'description')

# # ---------- UserLog Admin ----------
# @admin.register(UserLog)
# class UserLogAdmin(admin.ModelAdmin):
#     list_display = ('user', 'action', 'timestamp')
#     list_filter = ('user', 'timestamp')
#     search_fields = ('user__username', 'action')
#     ordering = ('-timestamp',)


# # ---------- Item Admin ----------
# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'is_active')
#     list_filter = ('is_active',)
#     search_fields = ('name',)
#     ordering = ('-price',)
#     fields = ('name', 'price', 'description', 'image', 'is_active')


# # ---------- Table Admin ----------
# @admin.register(Table)
# class TableAdmin(admin.ModelAdmin):
#     list_display = ('number', 'max_seats', 'reserved', 'reserved_by')
#     list_filter = ('reserved',)
#     search_fields = ('number', 'reserved_by__username')
#     ordering = ('number',)
#     actions = ['release_tables']

#     @admin.action(description="Освободить выбранные столы")
#     def release_tables(self, request, queryset):
#         for table in queryset:
#             table.release()


# # ---------- Order Admin ----------
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'status', 'created_at', 'total_price', 'in_restaurant', 'table')
#     list_filter = ('status', 'in_restaurant', 'created_at')
#     search_fields = ('user__username', 'id')
#     ordering = ('-created_at',)
#     readonly_fields = ('total_price', 'created_at', 'updated_at')
#     fieldsets = (
#         ('Основная информация', {
#             'fields': ('user', 'items', 'status', 'in_restaurant', 'table', 'total_price')
#         }),
#         ('Временные метки', {
#             'fields': ('created_at', 'updated_at')
#         }),
#     )


# # ---------- Computer Admin ----------
# @admin.register(Computer)
# class ComputerAdmin(admin.ModelAdmin):
#     list_display = ('name', 'in_use')
#     list_filter = ('in_use',)
#     search_fields = ('name', 'specs')
#     ordering = ('name',)


# # ---------- Tariff Admin ----------
# @admin.register(Tariff)
# class TariffAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'duration', 'speed')


# # Создание тарифов после миграции
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from .models import Game

# class GameAdmin(admin.ModelAdmin):
#     list_display = ('title', 'genre', 'difficulty', 'language', 'single_player', 'multiplayer')
#     list_filter = ('difficulty', 'language', 'genre')
#     search_fields = ('title', 'description')

# admin.site.register(Game, GameAdmin)
# @receiver(post_migrate)
# def create_default_tariffs(sender, **kwargs):
#     if sender.name == 'cafe_app':  # Убедитесь, что сигнал срабатывает только для вашего приложения
#         Tariff.objects.get_or_create(name="Базовый", speed=10, price=100, duration=1)
#         Tariff.objects.get_or_create(name="Продвинутый", speed=50, price=200, duration=1)
#         Tariff.objects.get_or_create(name="Премиум", speed=100, price=300, duration=1)












from django.contrib import admin
from .models import (
    UserLog, Game, MenuCategory, MenuItem, UserProfile, Table, Order,
    Tariff, UserSession, Promotion, Item, Computer
)

# Логирование действий пользователей
@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'action')


# Модель игры
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'difficulty', 'language', 'single_player', 'multiplayer')
    list_filter = ('genre', 'difficulty', 'language', 'single_player', 'multiplayer')
    search_fields = ('title', 'description', 'genre')


# Модели меню и товаров
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')


# Профиль пользователя
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'avatar')
    search_fields = ('user__username', 'phone')


# Стол и заказ
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'max_seats', 'reserved', 'reserved_by')
    list_filter = ('reserved',)
    search_fields = ('number', 'reserved_by__username')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'in_restaurant', 'created_at')
    list_filter = ('status', 'in_restaurant', 'created_at')
    search_fields = ('user__username', 'status')
    date_hierarchy = 'created_at'


# Тарифы и сессии
@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    search_fields = ('name',)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('user__username', 'session_key')


# Промоции
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')


# Товары
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


# Компьютеры
@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('name', 'in_use')
    list_filter = ('in_use',)
    search_fields = ('name', 'specs')
