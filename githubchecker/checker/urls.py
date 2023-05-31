from django.urls import path

from .views import PullRequestMetricsAPIView


urlpatterns = [
    path('metrics/pull-request/<int:repository_id>', PullRequestMetricsAPIView.as_view()),
]
