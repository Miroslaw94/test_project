import json

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .helpers import excel_columns_calculator


class CalculateView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        excel_file = request.data['file']

        column_names = json.loads(request.POST['columns'])
        column_names = [col.strip() for col in column_names]

        return Response(excel_columns_calculator(excel_file, column_names), status=204)
