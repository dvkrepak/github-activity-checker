from enum import Enum
from .models import PullRequestMetrics

import requests
import json


class EventTypes(Enum):
    WatchEvent = 'WatchEvent'
    PullRequestEvent = 'PullRequestEvent'
    IssuesEvent = 'IssuesEvent'


class GHParser:

    def __init__(self):
        self.last_parsed_time = None

    @staticmethod
    def __calculate_average_pull_request(repository_name: str):
        average_time = 0

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
        #  TODO: Parse until last time < time of parse start
        response = requests.get('https://api.github.com/events', headers={'Authorization': token})
        data = json.loads(response.text)
        for event in data:

            try:
                event_type: EventTypes = EventTypes(event['type'])
            except ValueError:
                # Event that we do not want to collect information about
                # For example: `PushEvent`
                continue

            repo_id = event['repo']['id']
            repo_name = event['repo']['name']
            print(f'Type = {event_type}; repo_id = {repo_id}; repo_name = {repo_name}')


if __name__ == '__main__':
    TOKEN = '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'
    GHParser.parse(TOKEN)
    GHParser.calculate_average_request_time("", 'WatchEvent')
