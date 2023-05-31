from enum import Enum

import django.db.utils

from .models import PullRequestMetrics, Repository, Event
from django.db.models import Avg
from django.utils import timezone

import requests
import json


class EventTypes(Enum):
    WatchEvent = 'WatchEvent'
    PullRequestEvent = 'PullRequestEvent'
    IssuesEvent = 'IssuesEvent'


class GHParser:

    last_parsed_datetime = None

    @staticmethod
    def __calculate_average_pull_request(repository_name: str):
        repository = Repository.objects.get(name=repository_name)
        pull_requests = repository.events.filter(event_type=Event.PULL_REQUEST_EVENT)
        average_time = pull_requests.aggregate(avg_time=Avg('created_at'))['avg_time']

        data = {
            'repository_name': repository_name,
            'average_pull_request_time': average_time,
        }
        metrics = PullRequestMetrics(respond=average_time)
        metrics.save()
        return data

    @staticmethod
    def calculate_average_request_time(repository_name: str, parse_type: str):
        eventType: EventTypes = EventTypes(parse_type)

        if eventType == EventTypes.PullRequestEvent:
            return GHParser.__calculate_average_pull_request(repository_name)

        if eventType == EventTypes.IssuesEvent or eventType == EventTypes.WatchEvent:
            raise TypeError(f'Cannot calculate {parse_type} yet')

        raise TypeError(f'Incorrect parse type `{parse_type}` for time request')

    @staticmethod
    def parse(token: str):
        response = requests.get('https://api.github.com/events', headers={'Authorization': token})
        data = json.loads(response.text)
        new_datetime = None
        for event in data:
            try:
                event_type: EventTypes = EventTypes(event['type'])
            except ValueError:
                # Event that we do not want to collect information about
                # For example: `PushEvent`
                continue
            except TypeError:
                """
                Crossed the limit of possible requests
                For fixing this problem check 
                https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting
                """
                raise ConnectionError("We've crossed the limit of possible messages.\nUser access token requests are li"
                                      "mited to 5,000 requests per hour and per authenticated user. ")

            repo_id = event['repo']['id']
            repo_name = event['repo']['name']
            event_datetime = event['created_at']

            if new_datetime is None:
                new_datetime = event_datetime

            if GHParser.last_parsed_datetime is not None and event_datetime <= GHParser.last_parsed_datetime:
                break

            event_instance = Event.objects.create(
                event_type=event_type.name,
                created_at=timezone.now()
            )
            event_instance.save()

            repository, _ = Repository.objects.get_or_create(repo_id=repo_id, defaults={'name': repo_name})
            repository.events = event_instance
            repository.save()

        GHParser.last_parsed_datetime = new_datetime
