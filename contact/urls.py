from django.urls import path
from .views import contact_us_api

urlpatterns = [
    path("send-message/", contact_us_api, name="contact-api"),
]
