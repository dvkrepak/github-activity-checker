from enum import Enum
from .models import PullRequestMetrics

import requests
import json




class EventTypes(Enum):
    WatchEvent = 'WatchEvent'
    PullRequestEvent = 'PullRequestEvent'
    IssuesEvent = 'IssuesEvent'


class GHParser:

    @staticmethod
    def __calculate_average_watch_request(repository_name: str):
        pass

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
    def __calculate_average_issues_request(repository_name: str):
        pass

    @staticmethod
    def calculate_average_request_time(repository_name: str, parse_type: str):
        eventType: EventTypes = EventTypes(parse_type)

        if eventType == EventTypes.WatchEvent:
            return GHParser.__calculate_average_watch_request(repository_name)

        if eventType == EventTypes.PullRequestEvent:
            return GHParser.__calculate_average_pull_request(repository_name)

        if eventType == EventTypes.IssuesEvent:
            return GHParser.__calculate_average_issues_request(repository_name)
        return {}

    @staticmethod
    def parse(token: str):
        response = requests.get('https://api.github.com/events', headers={'Authorization': token})
        data = json.loads(response.text)
        for event in data:
            event_type: EventTypes = EventTypes(event['type'])
            repo_id = event['repo']['id']
            repo_name = event['repo']['name']
            print(f'Type = {event_type}; repo_id = {repo_id}; repo_name = {repo_name}')


if __name__ == '__main__':
    TOKEN = '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'
    # GHParser.parse(TOKEN)
    GHParser.calculate_average_request_time("", 'WatchEvent')
