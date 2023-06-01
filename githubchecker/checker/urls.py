from django.urls import path

from .views import PullRequestMetricsAPIView


urlpatterns = [
    path('metrics/pull-request/<int:repo_id>', PullRequestMetricsAPIView.as_view()),
]
