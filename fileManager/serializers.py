from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    image_id = serializers.CharField(required=True)
