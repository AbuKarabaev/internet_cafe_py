from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MenuCategory, MenuItem, UserProfile, Order, Computer, Promotion, Game, Table, Tariff, UserLog, UserSession
from .serializers import ComputerSerializer, ItemSerializer, TableSerializer, UserLogSerializer, OrderSerializer
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from .models import Drink
from .models import Cheesecake
from .models import Dish
from .models import Offer

def offers_list(request):
    offers = Offer.objects.all()
    return render(request, 'offers_list.html', {'offers': offers})


def dish_view(request):
    dishes = Dish.objects.all()  # Получаем все блюда из базы данных
    return render(request, 'dish.html', {'dishes': dishes})
def cheesecake_view(request):
    # Получаем все чизкейки из базы данных
    cheesecakes = Cheesecake.objects.all()

    # Пагинация или фильтрация, если нужно
    sort_by = request.GET.get('sort_by', 'name')  # Сортировка по имени или цене
    if sort_by == 'price':
        cheesecakes = cheesecakes.order_by('price')
    else:
        cheesecakes = cheesecakes.order_by('name')

    return render(request, 'cheesecake.html', {'cheesecakes': cheesecakes})
def drink_list(request):
    drinks = Drink.objects.all()
    return render(request, 'drinks/drink_list.html', {'drinks': drinks})
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Function-based Views
def menu_view(request):
    """Отображение меню с категориями и пунктами меню."""
    categories = MenuCategory.objects.all()
    items = MenuItem.objects.all()
    user_profile = UserProfile.objects.filter(user=request.user).first()
    orders = Order.objects.filter(user=request.user)

    context = {
        'categories': categories,
        'items': items,
        'user_profile': user_profile,
        'orders': orders,
    }
    return render(request, 'menu.html', context)

def promotion_list(request):
    """Display a list of promotions."""
    promotions = Promotion.objects.all()
    return render(request, 'promotion_list.html', {'promotions': promotions})

def promotion_detail(request, promotion_id):
    """Display a specific promotion detail."""
    promotion = get_object_or_404(Promotion, id=promotion_id)
    return render(request, 'promotion_detail.html', {'promotion': promotion})

def game_list(request):
    """Display a list of games."""
    games = Game.objects.all()
    return render(request, 'game_list.html', {'games': games})

def services_view(request):
    """Display available tariffs."""
    tariffs = Tariff.objects.all()
    return render(request, 'services.html', {'tariffs': tariffs})

def select_tariff(request, tariff_id):
    """Select a tariff for the user."""
    if request.method == 'POST':
        tariff = get_object_or_404(Tariff, id=tariff_id)
        user_session, created = UserSession.objects.get_or_create(user=request.user)
        user_session.tariff = tariff
        user_session.remaining_time = tariff.duration * 60  # Duration in seconds
        user_session.save()
        return JsonResponse({'message': f'Tariff "{tariff.name}" selected.', 'remaining_time': user_session.remaining_time})
    return JsonResponse({'error': 'Invalid method. POST required.'}, status=400)

def extend_time(request):
    """Extend the user session time."""
    if request.method == 'POST':
        user_session = get_object_or_404(UserSession, user=request.user)
        additional_time = int(request.POST.get('minutes', 30)) * 60  # Convert minutes to seconds
        user_session.remaining_time += additional_time
        user_session.save()
        return JsonResponse({'message': f'Time extended by {additional_time // 60} minutes.', 'remaining_time': user_session.remaining_time})
    return JsonResponse({'error': 'Invalid method. POST required.'}, status=400)

# Class-based Views
class IndexView(TemplateView):
    template_name = 'index.html'

class TablesView(TemplateView):
    template_name = 'tables.html'

class StatisticsView(TemplateView):
    template_name = 'statistics.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

def cart_view(request):
    """Render the shopping cart page."""
    return render(request, 'cart.html')

# ViewSets for CRUD operations
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['put'], url_path='confirm')
    def confirm_order(self, request, pk=None):
        """Confirm an order."""
        order = self.get_object()
        if order.status == 'completed':
            return Response({"error": "Order already completed."}, status=400)
        order.status = 'confirmed'
        order.save()
        return Response({"status": "Order confirmed successfully."})

# Tables
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['put'], url_path='reserve')
    def reserve(self, request, pk=None):
        """Reserve a table for the user."""
        table = self.get_object()
        if table.reserved:
            return Response({"error": "Table already reserved."}, status=400)

        table.reserved = True
        table.reserved_by = request.user
        table.save()
        return Response({"status": "Table reserved successfully."})

# Computers
class ComputerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['put'], url_path='toggle')
    def toggle_status(self, request, pk=None):
        """Toggle the computer's active status."""
        computer = self.get_object()
        computer.is_active = not computer.is_active
        computer.save()
        return Response({'status': f'Computer {"activated" if computer.is_active else "deactivated"}.'})

# User Logs
class UserLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.all()
    serializer_class = UserLogSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='logs')
    def logs(self, request):
        """Retrieve user logs."""
        user_logs = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_logs, many=True)
        return Response(serializer.data)
