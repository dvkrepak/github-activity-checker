from rest_framework import generics

from .models import Repository, Event
from .serializers import RepositorySerializer, EventSerializer


class RepositoryAPIView(generics.ListAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()


class RepositoryDetailAPIView(generics.ListAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.filter()

