from rest_framework import serializers

class SnipperSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)