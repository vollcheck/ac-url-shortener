from rest_framework import serializers

class ShortURLSerializer(serializers.Serializer):
    url = serializers.URLField()
