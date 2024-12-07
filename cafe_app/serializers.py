from rest_framework import serializers
from .models import Item, Table, Order, Computer, UserLog
from rest_framework import serializers
from .models import Computer
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = '__all__'
from rest_framework import serializers
from .models import UserLog

class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'image']

    def validate_price(self, value):
        """Ensure that the price is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value


class TableSerializer(serializers.ModelSerializer):
    reserved_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Table
        fields = ['id', 'number', 'max_seats', 'reserved', 'reserved_by']

    def validate_max_seats(self, value):
        """Ensure that a table has at least two seats."""
        if value < 2:
            raise serializers.ValidationError("Минимальное количество мест за столом - 2.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=True)
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), required=False)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'created_at', 'updated_at', 'in_restaurant', 'table', 'status', 'total_price']

    def validate(self, data):
        """Ensure valid order data."""
        if data.get('in_restaurant') and not data.get('table'):
            raise serializers.ValidationError("Если заказ в ресторане, стол должен быть выбран.")
        if not data.get('items'):
            raise serializers.ValidationError("В заказе должны быть товары.")
        return data

    def create(self, validated_data):
        order = super().create(validated_data)
        if order.table and order.in_restaurant:
            order.table.reserve(order.user)
        return order

    def update(self, instance, validated_data):
        """Handle table reservation changes on update."""
        new_table = validated_data.get('table', instance.table)
        if new_table != instance.table:
            if instance.table:
                instance.table.reserved = False
                instance.table.reserved_by = None
                instance.table.save()
            if new_table:
                new_table.reserve(instance.user)
            instance.table = new_table
        return super().update(instance, validated_data)
