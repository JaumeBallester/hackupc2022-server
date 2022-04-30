from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse

from drf_yasg.utils import swagger_auto_schema

from motorbikes.serializers import *
from motorbikes.models import Motorbikes, Brands 
import random
from tabulate import tabulate

def bikeToDict(bike):

    return  {
            'id' : bike.bike_id,
            'name' : bike.name,
            'brand' : bike.brand.name,
            'year' : bike.year,
            'km' : bike.km,
            'type' : bike.type,
            'licence' : bike.licence,
            'old_price' : bike.old_price,
            'price' : bike.price,
            'cc' : bike.cc,
            'url' : bike.url
        }

class Bike(APIView):

    @swagger_auto_schema(responses={200: MotorbikeSerializer(many=False)})
    def get(self, request, bike_id, format=None):


        bike = Motorbikes.objects.get(bike_id=bike_id)

        if not bike:
            return Response( {}, status=status.HTTP_200_OK)

        response = bikeToDict(bike)

        mps = MotorbikeSerializer(data=response, many=False)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)


class Bikes(APIView):

    @swagger_auto_schema(request_body=BikeSelectorSerializer, responses={200: MotorbikeSerializer(many=True)})
    def post(self, request, format=None):

        in_data = BikeSelectorSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)
        bike_ids = in_data.validated_data.get('bike_ids')

        bikes = Motorbikes.objects.filter(bike_id__in=bike_ids)

        if not bikes:
            return Response( [], status=status.HTTP_200_OK)

        response = [bikeToDict(bike) for bike in bikes]

        mps = MotorbikeSerializer(data=response, many=True)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)

def pickRandomDict(my_dict):
    return random.choices(list(my_dict.keys()), weights=my_dict.values(), k=1)[0]

def getBikesRange(bikes, field, range):
    field_range = range.split('-')
    field_min = int(field_range[0])
    field_max = int(field_range[1])
    return set(bike['bike_id'] for bike in bikes if field_max>=bike[field] and bike[field]>=field_min)


class NextBike(APIView):

    @swagger_auto_schema(request_body=NextBikeSerializer, responses={200: MotorbikeSerializer(many=False)})
    def post(self, request, format=None):

        in_data = NextBikeSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)
        exclude = in_data.validated_data.get('exclude')
        year    = in_data.validated_data.get('year')
        price    = in_data.validated_data.get('price')
        km    = in_data.validated_data.get('km')
        cc    = in_data.validated_data.get('cc')


        bikes = [bike.__dict__ for bike in Motorbikes.objects.all().exclude(bike_id__in=exclude)]

        year_range = pickRandomDict(year)
        price_range = pickRandomDict(price)
        km_range = pickRandomDict(km)
        cc_range = pickRandomDict(cc)

        year_bikes = getBikesRange(bikes, 'year', year_range)
        price_bikes = getBikesRange(bikes, 'price', price_range)
        km_bikes = getBikesRange(bikes, 'km', km_range)
        cc_bikes = getBikesRange(bikes, 'cc', cc_range)


        intersection_bikes1 = year_bikes.intersection(price_bikes)
        intersection_bikes2 = intersection_bikes1.intersection(km_bikes)
        intersection_bikes3 = intersection_bikes2.intersection(cc_bikes)

        bike_id = intersection_bikes3.pop()
        result_bike=bikeToDict(Motorbikes.objects.get(bike_id=bike_id))

        print()
        print(tabulate(
            [['Year',year_range, len(year_bikes), result_bike['year']],
            [ 'Price',price_range, len(price_bikes), result_bike['price']],
            [ 'Km',km_range, len(km_bikes), result_bike['km']],
            [ 'cc', cc_range, len(cc_bikes), result_bike['cc']]],
            headers=["Field", "Range", "Included", "Selected"]))
        print()

        mps = MotorbikeSerializer(data=result_bike, many=False)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)