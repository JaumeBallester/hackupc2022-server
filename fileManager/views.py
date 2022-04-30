from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema

from fileManager.serializers import *

import hack22server.constants as CT
from django.http import FileResponse

import base64

class Image(APIView):

    @swagger_auto_schema(content_type="image/jpg")
    def get(self, request, image_id, format=None):
        #in_data = ImageSerializer(data=request.data)
        #in_data.is_valid(raise_exception=True)


        #image_id  = in_data.validated_data.get('image_id')

        try:
            imgPath = CT.IMAGES_DIR + image_id +".jpg"
            img = open(imgPath, 'rb')
            response = FileResponse(img)
            return response

        except IOError:
            return Response( {'Error': "File not Found"}, status=status.HTTP_200_OK)



