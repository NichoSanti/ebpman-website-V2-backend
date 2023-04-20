from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from .models import Contact
from .serializers import ContactSerializer
from django.conf import settings


@api_view(['GET'])
def getRoutes(request):

    return Response('Our API')


@api_view(['POST'])
def createContact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        first_name = serializer.validated_data['first_name']
        last_name = serializer._validated_data['last_name']
        email = serializer.validated_data['email_address']
        message = serializer.validated_data['message']

        send_email(first_name, last_name, email, message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email(first_name, last_name, email, message):
    subject = 'New contact form submission'
    from_email = 'your_email@example.com'  # Replace with your own email
    to_email = settings.DEFAULT_FROM_EMAIL  # Replace with the recipient's email
    body = f"Name: {first_name} {last_name}\nEmail: {email}\nMessage: {message}"

    send_mail(subject, body, from_email, [to_email], fail_silently=False)


@api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all().order_by('-created')
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)
