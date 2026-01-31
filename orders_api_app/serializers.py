from rest_framework import serializers
from .models import Order, OrderItem
from menuItems_api_app.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class OrderHistorySerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "restaurant_name",
            "order_items",
            "totalAmount",
            "status",
            "createdAt"
        ]