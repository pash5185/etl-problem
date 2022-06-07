from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from etl_app.models import SampleData
from etl_app.serializers import SampleDataSerializer
from etl_app.utils import StandardResultsSetPagination


class SampleDataViewSet(GenericViewSet, ListModelMixin):
    permission_classes = []
    authentication_classes = []
    pagination_class = StandardResultsSetPagination
    serializer_class = SampleDataSerializer
    queryset = SampleData.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quality',]
