from enum import Enum
from datetime import timedelta

from .models import PullRequestMetrics, Repository, Event, EventType
from django.db.models import Func, FloatField, DateTimeField
from django.utils import timezone

import requests
import json


class EventTypes(Enum):
    WatchEvent = 'WatchEvent'
    PullRequestEvent = 'PullRequestEvent'
    IssuesEvent = 'IssuesEvent'


class Epoch(Func):
    template = 'EXTRACT(epoch FROM %(expressions)s)::FLOAT'
    output_field = FloatField()


class DateTimeFromFloat(Func):
    template = 'To_TIMESTAMP(%(expressions)s)::TIMESTAMP at time zone \'UTC\''
    output_field = DateTimeField()


class GHParser:

    last_parsed_datetime = None

    @staticmethod
    def __calculate_average_pull_request(repository_id: int):
        try:
            repository = Repository.objects.get(gh_repo_id=repository_id)
            event_type = EventType.objects.get(event_type='PullRequestEvent')
            events = Event.objects.filter(repo=repository, event_type=event_type)
        except Repository.DoesNotExist:
            return 'No existing `repository`'
        except Event.DoesNotExist:
            return 'No existing `event`'
        except EventTypes.DoesNotExist:
            return 'No existing event type in database for `PullRequestEvent`'

        if len(events) < 2:
            return 0  # Difference between one / zero datetimes is zero

        total_difference = timedelta()
        for index in range(1, len(events)):
            difference = events[index].created_at - events[index - 1].created_at
            total_difference += difference

        average_difference = total_difference / (len(events) - 1)

        days = average_difference.days
        hours, remainder = divmod(average_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        average_difference_str = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
        return average_difference_str

    @staticmethod
    def calculate_average_request_time(repository_id: int, parse_type: str):
        eventType: EventTypes = EventTypes(parse_type)

        if eventType == EventTypes.PullRequestEvent:
            return GHParser.__calculate_average_pull_request(repository_id)

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
                                      "mited to 5,000 requests per hour.")

            repo_id = event['repo']['id']
            repo_name = event['repo']['name']
            event_datetime = event['created_at']

            if new_datetime is None:
                new_datetime = event_datetime

            if GHParser.last_parsed_datetime is not None and event_datetime <= GHParser.last_parsed_datetime:
                break

            repository, _ = Repository.objects.get_or_create(repo_id=repo_id, defaults={'name': repo_name})
            event_type_instance, _ = Event.objects.get_or_create(event_type=event_type)

            event_instance = Event.objects.create(
                event_type=event_type_instance,
                repo=repository,
                created_at=timezone.now()
            )
            event_instance.save()
            repository.save()

        GHParser.last_parsed_datetime = new_datetime
