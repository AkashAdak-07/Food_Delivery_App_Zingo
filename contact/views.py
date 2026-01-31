from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer

# Create your views here.



@api_view(["POST"])
def contact_us_api(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        contact = serializer.save()

        # Send email to admin
        send_mail(
            subject=f"[Contact Us] {contact.subject}",
            message=(
                f"Name: {contact.full_name}\n"
                f"Email: {contact.email}\n\n"
                f"Message:\n{contact.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(
            {"message": "Message sent successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
