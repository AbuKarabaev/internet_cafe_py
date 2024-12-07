from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ItemViewSet,
    TableViewSet,
    OrderViewSet,
    IndexView,
    TablesView,
    StatisticsView,
    ProfileView,
    cart_view,
    menu_view,
    game_list,
    promotion_list,
    services_view,
    select_tariff,
    extend_time
)

# ---------- API Router Setup ----------
router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'orders', OrderViewSet, basename='orders')

# ---------- URL Patterns ----------
urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),  # Including API routes via router
    # Main Pages (HTML views)
    path('', IndexView.as_view(), name='index'),  # Home page
    path('tables/', TablesView.as_view(), name='tables'),  # Table selection
    path('statistics/', StatisticsView.as_view(), name='statistics'),  # Statistics page
    path('profile/', ProfileView.as_view(), name='profile'),  # User profile
    path('cart/', cart_view, name='cart'),  # Cart page
    path('menu/', views.menu_view, name='menu'),
    path('cheesecake/', views.cheesecake_view, name='cheesecake'),
    path('drinks/', views.drink_list, name='drink_list'),
    path('games/', game_list, name='game_list'),  # Game list page
    path('promotions/', promotion_list, name='promotion_list'),  # Promotions page
    path('dish/', views.dish_view, name='dish'),
    path('offers_list/', views.offers_list, name='offers_list'),
    # Services and Tariffs
    path('services/', services_view, name='services'),
    path('select-tariff/<int:tariff_id>/', select_tariff, name='select_tariff'),
    path('extend-time/', extend_time, name='extend_time'),
]

# Additional API Endpoints with Versioning
api_patterns = [
    path('items/', ItemViewSet.as_view({'get': 'list'}), name='item-list'),
    path('tables/', TableViewSet.as_view({'get': 'list'}), name='table-list'),
    path('orders/', OrderViewSet.as_view({'get': 'list'}), name='order-list'),
]

# Adding versioned API routes
urlpatterns += [
    path('api/v1/', include((api_patterns, 'api'), namespace='api-v1')),  # Versioned API routes
]
