from rest_framework import serializers

from .models import Repository, Event, PullRequestMetrics


class RepositorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository
        fields = ('pk', 'name', )


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('pk', 'event_type', 'created_at', )


class MetricsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PullRequestMetrics
        fields = ('id', 'respond', )
