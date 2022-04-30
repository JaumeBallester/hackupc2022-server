from rest_framework import serializers


class MotorbikeSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    id        = serializers.CharField(required=True)
    name      = serializers.CharField(required=True)
    brand     = serializers.CharField(required=True)
    year      = serializers.IntegerField(required=True)
    km        = serializers.IntegerField(required=True)
    type      = serializers.CharField(required=True)
    licence   = serializers.CharField(required=True)
    old_price = serializers.IntegerField(required=True, allow_null=True)
    price     = serializers.IntegerField(required=True)
    cc        = serializers.IntegerField(required=True)
    url       = serializers.CharField(required=True)

class NextBikeSerializer(serializers.Serializer):
    exclude = serializers.ListField(required=True)
    year = serializers.DictField(required=True)
    price = serializers.DictField(required=True)
    km = serializers.DictField(required=True)
    cc = serializers.DictField(required=True)
    brand = serializers.DictField(required=True)
    licence = serializers.DictField(required=True)
    type = serializers.DictField(required=True)

class NextBike2Serializer(serializers.Serializer):
    medians = serializers.DictField(required=True)
    filters = serializers.DictField(required=True)
    totalValuated = serializers.IntegerField(required=True)
    exclude = serializers.ListField(required=True)
    sent = serializers.ListField(required=True)

class BikeSelectorSerializer(serializers.Serializer):
    bike_ids = serializers.ListField(required=True)

class BikeStatsSerializer(serializers.Serializer):
    year      = serializers.ListField(required=True)
    km        = serializers.IntegerField(required=True)
    price     = serializers.IntegerField(required=True)
    cc        = serializers.IntegerField(required=True)
