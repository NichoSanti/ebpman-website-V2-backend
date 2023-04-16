from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from .models import Contact
from .serializers import ContactSerializer


@api_view(['GET'])
def getRoutes(request):

    return Response('Our API')


@api_view(['POST'])
def createContact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        message = serializer.validated_data['message']

        send_email(name, email, message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email(name, email, message):
    subject = 'New contact form submission'
    from_email = 'your_email@example.com' # Replace with your own email
    to_email = 'recipient@example.com' # Replace with the recipient's email
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    send_mail(subject, body, from_email, [to_email], fail_silently=False)




@api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all().order_by('-created')
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)