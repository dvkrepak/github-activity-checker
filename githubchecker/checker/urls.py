from django.urls import path

from .views import RepositoryAPIView, RepositoryDetailAPIView


urlpatterns = [
    path('stats/', RepositoryAPIView.as_view()),
    path('stats/<str:name>', RepositoryDetailAPIView.as_view()),
]
