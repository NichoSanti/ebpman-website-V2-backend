from rest_framework import serializers
from api.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email_address', 'updated']

