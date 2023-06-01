from django.urls import path

from .views import pull_request_metrics, events_metrics


urlpatterns = [
    path('metrics/pull-request/<int:repo>', pull_request_metrics),
    path('metrics/events/<int:offset>', events_metrics),
]
