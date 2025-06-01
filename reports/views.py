from rest_framework import viewsets
from rest_framework.response import Response
from .models import Rapport, RapportData
from .serializars import RapportSerializer, RapportDataSerializer

class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # Log serializer validation errors
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def get_queryset(self):
        user_param = self.request.query_params.get('user', None)
        if user_param:
            return self.queryset.filter(user=user_param)
        return self.queryset

class RapportDataViewSet(viewsets.ModelViewSet):
    queryset = RapportData.objects.all()
    serializer_class = RapportDataSerializer

    def get_queryset(self):
        report_param = self.request.query_params.get('rapport', None)
        if report_param:
            return self.queryset.filter(rapport_id=report_param)
        return self.queryset
