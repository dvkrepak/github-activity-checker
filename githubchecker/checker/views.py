from rest_framework import generics

from .models import Repository, PullRequestMetrics
from .serializers import RepositorySerializer, MetricsSerializer
from .utils import GHParser


class RepositoryAPIView(generics.ListAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()


class RepositoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.filter()


class MetricsAPIView(generics.RetrieveAPIView):
    serializer_class = MetricsSerializer
    lookup_field = 'repo_id'


class PullRequestMetricsAPIView(MetricsAPIView):
    queryset = Repository.objects.filter()
    if queryset.exists():
        repository = queryset.first()  # Retrieve the first Repository object from the queryset
        GHParser.calculate_average_request_time(repository.name, 'PullRequestEvent')
