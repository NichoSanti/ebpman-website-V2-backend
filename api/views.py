from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Contact
from .serializers import ContactSerializer

# Create your views here.
@api_view(['POST'])
def sendContact(request):
    data = request.data
    contact = Contact.objects.create(
        body=data['body']
    )
    serializer = ContactSerializer(contact, many=False)
    return Response(serializer.data)