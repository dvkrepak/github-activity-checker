from rest_framework import generics
from django.http import JsonResponse
from django.core import serializers

from .models import Repository, PullRequestMetrics
from .serializers import RepositorySerializer, MetricsSerializer
from .utils import GHParser


class RepositoryAPIView(generics.ListAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()


class RepositoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.filter()


def pull_request_metrics(request, repo: int):
    average_time = GHParser.calculate_average_request_time(repo, 'PullRequestEvent')
    response_data = {
        'github_repository_id': repo,
        'average_time': average_time
    }
    return JsonResponse(response_data)


def events_metrics(request, offset: int):
    response_data = GHParser.get_number_of_events_groupped(offset)
    return JsonResponse(response_data)
