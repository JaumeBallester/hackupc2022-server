from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse

from drf_yasg.utils import swagger_auto_schema

from motorbikes.serializers import *
from motorbikes.models import Motorbikes, Brands 


class Bike(APIView):

    @swagger_auto_schema(responses={200: MotorbikeSerializer(many=False)})
    def get(self, request, bike_id, format=None):


        bike = Motorbikes.objects.filter(bike_id=bike_id)

        if not bike:
            return Response( {}, status=status.HTTP_200_OK)

        response = {
            'id' : bike.bike_id,
            'name' : bike.name,
            'brand' : bike.brand,
            'year' : bike.year,
            'km' : bike.km,
            'type' : bike.type,
            'licence' : bike.licence,
            'old_price' : bike.old_price,
            'price' : bike.price,
            'cc' : bike.cc,
            'url' : bike.url
        }
        mps = MotorbikeSerializer(data=response, many=False)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)