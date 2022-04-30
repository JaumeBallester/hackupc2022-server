from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    testCharField = serializers.CharField(required=True)
    testInteger = serializers.IntegerField(required=True)

class TestResponseSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    testResponseListField = serializers.ListField(required=True)
    testInteger = serializers.IntegerField(required=True)
