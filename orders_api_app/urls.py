from django.urls import path
from .views import place_order, track_order, update_order_status,user_order_history

urlpatterns = [
    path("place-order/", place_order),
    path("track-order/<int:order_id>/", track_order),
    path("update-status/<int:order_id>/", update_order_status),
    path("order-history/", user_order_history),
]
