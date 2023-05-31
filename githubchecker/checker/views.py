from rest_framework import generics

from .models import Repository, PullRequestMetrics
from .serializers import RepositorySerializer, PullRequestMetricsSerializer


class RepositoryAPIView(generics.ListAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()


class RepositoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.filter()


class PullRequestMetricsAPIView(generics.RetrieveAPIView):
    serializer_class = PullRequestMetricsSerializer
    queryset = PullRequestMetrics.objects.filter()
    lookup_field = 'repository_id'
