from rest_framework import serializers


class MotorbikeSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    id        = serializers.CharField(required=True)
    name      = serializers.CharField(required=True)
    brand     = serializers.ForeignKey(required=True)
    year      = serializers.IntegerField(required=True)
    km        = serializers.IntegerField(required=True)
    type      = serializers.CharField(required=True)
    licence   = serializers.CharField(required=True)
    old_price = serializers.IntegerField(required=True, allow_null=True)
    price     = serializers.IntegerField(required=True)
    cc        = serializers.IntegerField(required=True)
    url       = serializers.CharField(required=True)
    image     = serializers.CharField(required=True)