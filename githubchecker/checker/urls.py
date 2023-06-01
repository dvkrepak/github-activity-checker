from django.urls import path

from .views import pull_request_metrics, events_metrics, events_metrics_visualization


urlpatterns = [
    path('metrics/pull-request/<int:repo>', pull_request_metrics),
    path('metrics/events/<int:offset>', events_metrics),
    path('metrics/events_visualization/<int:offset>', events_metrics_visualization),
]
