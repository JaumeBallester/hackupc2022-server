from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from userData.serializers import *
from drf_yasg.utils import swagger_auto_schema

class Test(APIView):

    @swagger_auto_schema(request_body=TestSerializer, responses={200: TestResponseSerializer(many=False)})
    def post(self, request, format=None):
        """
        This is a test API call.
        """
        in_data = TestSerializer(data=request.data)
        in_data.is_valid(raise_exception=True)

        testCharField    = in_data.validated_data.get('testCharField')
        testInteger    = in_data.validated_data.get('testInteger')

        response = { "testResponseListField": [testCharField],
                     "testInteger": testInteger}

        mps = TestResponseSerializer(data=response, many=False)

        if mps.is_valid():
            return Response(mps.data, status=status.HTTP_200_OK)

        return Response(mps.errors, status=status.HTTP_400_BAD_REQUEST)
