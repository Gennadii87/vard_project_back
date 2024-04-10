from rest_framework import serializers


class UrlFileLoadSerializer(serializers.Serializer):
    url_load = serializers.URLField(required=True)
