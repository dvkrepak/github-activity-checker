from rest_framework import serializers

from .models import Repository, Event


class RepositorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository
        fields = ('pk', 'name', )


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('pk', 'event_type', 'repository_id', 'created_at', )

