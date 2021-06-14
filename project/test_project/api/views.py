import json

from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from .helpers import excel_columns_calculator


class CalculateView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        try:
            excel_file = request.data['file']
        except MultiValueDictKeyError:
            message = {
                "error": "Excel file not found in request data. "
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        try:
            column_names = json.loads(request.POST['columns'])
            column_names = [col.strip() for col in column_names]
        except MultiValueDictKeyError:
            message = {
                "error": "Columns list not found in request data. "
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        try:
            return Response(excel_columns_calculator(excel_file, column_names), status=status.HTTP_200_OK)
        except ValueError:
            message = {
                "error": "Uploaded file is not a recognized excel file. "
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
