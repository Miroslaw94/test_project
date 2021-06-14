from rest_framework import serializers


class CalculateExcelSerializer(serializers.Serializer):
    file = serializers.FileField()
    columns = serializers.ListField(child=serializers.CharField())


class CalculateExcelSummarySerializer(serializers.Serializer):
    column = serializers.CharField()
    sum = serializers.FloatField()
    avg = serializers.FloatField()


class CalculateExcelResponseSerializer(serializers.Serializer):
    file = serializers.CharField()
    summary = serializers.ListField(child=CalculateExcelSummarySerializer())
