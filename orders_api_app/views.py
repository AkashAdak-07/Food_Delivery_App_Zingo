from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from cart_api_app.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderHistorySerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user   

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    cart_items = cart.cart_items.select_related("menu_item", "menu_item__restaurant")

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    restaurant = cart_items.first().menu_item.restaurant
    total_amount = 0

    order = Order.objects.create(
        user=user,
        restaurant=restaurant,
        totalAmount=0
    )

    for item in cart_items:
        price = item.menu_item.price
        total_amount += price * item.quantity

        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            price=price
        )

    order.totalAmount = total_amount
    order.save()

    cart.cart_items.all().delete()

    return Response(
        {"message": "Order placed successfully", "order_id": order.id},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=200)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    status_value = request.data.get("status")

    if not status_value:
        return Response({"error": "status is required"}, status=400)

    order = get_object_or_404(Order, id=order_id)
    order.status = status_value
    order.save()

    return Response({"message": "Order status updated"}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_order_history(request):
    user = request.user  

    orders = Order.objects.filter(user=user).order_by("-createdAt")
    serializer = OrderHistorySerializer(orders, many=True)

    return Response(
        {
            "user_id": user.id,
            "total_orders": orders.count(),
            "orders": serializer.data
        },
        status=200
    )
