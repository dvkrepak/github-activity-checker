from rest_framework import generics

from .models import Repository, PullRequestMetrics
from .serializers import RepositorySerializer, MetricsSerializer


class RepositoryAPIView(generics.ListAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()


class RepositoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.filter()


class MetricsAPIView(generics.RetrieveAPIView):
    serializer_class = MetricsSerializer
    lookup_field = 'repository_id'


class PullRequestMetricsAPIView(MetricsAPIView):
    queryset = PullRequestMetrics.objects.filter()
