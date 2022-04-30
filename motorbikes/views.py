from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse

from drf_yasg.utils import swagger_auto_schema

from motorbikes.serializers import *
from motorbikes.models import Motorbikes, Brands 
import random
from tabulate import tabulate
from django.db.models import Avg, Max, Min, Sum
import bisect 
import random
from operator import add, sub, mul


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
    return set(bike['id'] for bike in bikes if field_max>=bike[field] and bike[field]>=field_min)

def getBikesEquals(bikes, field, value):
    return set(bike['id'] for bike in bikes if bike[field] == value)


class BikeStats(APIView):

    @swagger_auto_schema(responses={200: BikeStatsSerializer(many=False)})
    def get(self, request, format=None):
        
        results ={}
        stats = Motorbikes.objects.all().aggregate(Avg('price'),
                                                 Max('price'),
                                                 Min('price'),
                                                 Avg('year'),
                                                 Max('year'),
                                                 Min('year'),
                                                 Avg('cc'),
                                                 Max('cc'),
                                                 Min('cc'),
                                                 Avg('km'),
                                                 Max('km'),
                                                 Min('km'))
        for stat in stats:
            keys = stat.split('__')
            if keys[0] not in results:
                results[keys[0]] = {}
            results[keys[0]][keys[1]] = stats[stat]
        return Response(results, status=status.HTTP_200_OK)


class NextBike(APIView):

    @swagger_auto_schema(request_body=NextBike2Serializer)
    def post(self, request, format=None):

        in_data = NextBike2Serializer(data=request.data)
        in_data.is_valid(raise_exception=True)
        exclude = in_data.validated_data.get('exclude')
        sent = in_data.validated_data.get('sent')

        exclude += sent

        userMean = in_data.validated_data.get('medians')
        numberBikes = in_data.validated_data.get('totalValuated')
        filters = in_data.validated_data.get('filters')

        excludeDic = {}
        for _filter in filters:
            excludeDic[_filter] = set([ c for c in filters[_filter] if not filters[_filter][c]])
        

        results = {}
        stats = Motorbikes.objects.all().aggregate(Avg('price'),
                                                 Max('price'),
                                                 Min('price'),
                                                 Avg('year'),
                                                 Max('year'),
                                                 Min('year'),
                                                 Avg('cc'),
                                                 Max('cc'),
                                                 Min('cc'),
                                                 Avg('km'),
                                                 Max('km'),
                                                 Min('km'))
        for stat in stats:
            keys = stat.split('__')
            if keys[0] not in results:
                results[keys[0]] = {}
            results[keys[0]][keys[1]] = stats[stat]
        
        # THIS SHOULD BE CACHED!
        unfiltered_bikes = {b['bike_id']:b for b in Motorbikes.objects.all().values('bike_id', 'price', 'year', 'cc', 'km', 'licence', 'type', 'brand') if b['bike_id'] not in set(exclude)}
        
        brands = {b.brand_id:b.name for b in Brands.objects.all()}
        bikes = {}
        # Exclude filters
        for bike in unfiltered_bikes:
            if (unfiltered_bikes[bike]['licence'] not in excludeDic['licence'] and 
               unfiltered_bikes[bike]['type'] not in excludeDic['type'] and
               brands[unfiltered_bikes[bike]['brand']] not in excludeDic['brand']):
                bikes[bike] = unfiltered_bikes[bike]
        
        # Normalize bikes values
        for field in ['price', 'year', 'cc', 'km']:
            for bike in bikes:
                bikes[bike][field] = (bikes[bike][field] - results[field]['min']) / (results[field]['max'] - results[field]['min'])
        
        #Normalize user Mean
        for field in userMean:
            userMean[field] = (userMean[field] - results[field]['min']) / (results[field]['max'] - results[field]['min'])
        

        #Calculate Distance from user

        bikeDistance = []
        for bike in bikes:
            distance = 0
            for field in ['price', 'year', 'cc', 'km']:
                distance += abs(userMean[field] - bikes[bike][field])
                #if bike == "0000000001":
                #    print(field, userMean[field], bikes[bike][field], abs(userMean[field] - bikes[bike][field]))

            random_range = max(0.3-(0.01*(numberBikes-1)),0.1)
            random_value = random.uniform(-random_range, +random_range)
            if distance/4 < abs(random_value) and random_value < 0:
                    distance = distance/4 
            else:
                distance = min( max( (distance/4) + random_value, 0) ,1)
            bisect.insort(bikeDistance, (distance, bike))

        #print(bikeDistance)

        if not bikeDistance:
            return Response({}, status=status.HTTP_200_OK)

        result_bike = bikeToDict(Motorbikes.objects.get(bike_id=bikeDistance[0][1]))

        mps = MotorbikeSerializer(data=result_bike, many=False)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)



class NextBikeOld(APIView):

    @swagger_auto_schema(request_body=NextBikeSerializer, responses={200: MotorbikeSerializer(many=False)})
    def post(self, request, format=None):

        in_data = NextBikeSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)
        exclude = in_data.validated_data.get('exclude')
        year    = in_data.validated_data.get('year')
        price    = in_data.validated_data.get('price')
        km    = in_data.validated_data.get('km')
        cc    = in_data.validated_data.get('cc')
        brand = in_data.validated_data.get('brand')
        type = in_data.validated_data.get('type')
        licence = in_data.validated_data.get('licence')


        bikes = [bikeToDict(bike) for bike in Motorbikes.objects.all().exclude(bike_id__in=exclude)]

        year_range = pickRandomDict(year)
        price_range = pickRandomDict(price)
        km_range = pickRandomDict(km)
        cc_range = pickRandomDict(cc)
        brand_value = pickRandomDict(brand)
        type_value = pickRandomDict(type)
        licence_value = pickRandomDict(licence)

        year_bikes = getBikesRange(bikes, 'year', year_range)
        price_bikes = getBikesRange(bikes, 'price', price_range)
        km_bikes = getBikesRange(bikes, 'km', km_range)
        cc_bikes = getBikesRange(bikes, 'cc', cc_range)
        
        brand_bikes = getBikesEquals(bikes, 'brand', brand_value)
        type_bikes = getBikesEquals(bikes, 'type', type_value)
        licence_bikes = getBikesEquals(bikes, 'licence', licence_value)

        key_debug = [[key,str(round(type[key]*100,2)) ] for key in type]

        print()
        print(tabulate(sorted(key_debug, key=lambda x: x[0]),tablefmt="pretty",headers=["Type", "Percent"]))
        print()
        bikes_sets = [year_bikes, price_bikes, km_bikes, cc_bikes, brand_bikes, type_bikes, licence_bikes]

        bike_scores = {}
        for b in bikes:
            bike_scores[b['id']] = sum([1 for set in bikes_sets if b['id'] in set])

        winners = sorted(bike_scores.items(), key=lambda x: x[1])[-3:]
        result_ids = [winner[0] for winner in winners]
        result_bikes = [bikeToDict(b) for b in Motorbikes.objects.filter(bike_id__in=result_ids)]

        print()
        print(tabulate(
            [['Year',   year_range,    len(year_bikes),    result_bikes[0]['year'],    result_bikes[0]['id'] in year_bikes ],
            [ 'Price',  price_range,   len(price_bikes),   result_bikes[0]['price'],   result_bikes[0]['id'] in price_bikes],
            [ 'Km',     km_range,      len(km_bikes),      result_bikes[0]['km'],      result_bikes[0]['id'] in km_bikes],
            [ 'cc',     cc_range,      len(cc_bikes),      result_bikes[0]['cc'],      result_bikes[0]['id'] in cc_bikes],
            [ 'brand',  brand_value,   len(brand_bikes),   result_bikes[0]['brand'],   result_bikes[0]['id'] in brand_bikes],
            [ 'type',   type_value,    len(type_bikes),    result_bikes[0]['type'],    result_bikes[0]['id'] in type_bikes],
            [ 'licence',licence_value, len(licence_bikes), result_bikes[0]['licence'], result_bikes[0]['id'] in licence_bikes],
            ],
            headers=["Field", "Range", "Included", "Selected", "Satisfies"],tablefmt="pretty"))
        print()
        print('TOTAL SCORE:', [winner[1] for winner in winners][::-1])
        print()

        mps = MotorbikeSerializer(data=result_bikes, many=True)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)