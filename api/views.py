from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all().order_by('-created')
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)