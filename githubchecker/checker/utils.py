from datetime import timedelta, datetime
from enum import Enum
from io import BytesIO

import json
import matplotlib
import requests
import numpy as np

from django.db.models import Count
from django.utils import timezone
from matplotlib import pyplot as plt

from .models import PullRequestMetrics, Repository, Event, EventType

matplotlib.use('Agg')  # Matplotlib settings


class EventTypes(Enum):
    """
    Enumeration representing different types of GitHub events.

    Values:
    - WatchEvent: Watch event type.
    - PullRequestEvent: Pull request event type.
    - IssuesEvent: Issues event type.
    """
    WatchEvent = 'WatchEvent'
    PullRequestEvent = 'PullRequestEvent'
    IssuesEvent = 'IssuesEvent'


class RateLimitExceededError(Exception):
    """
    Exception raised when the GitHub API rate limit has been exceeded.

    For fixing the problem check
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting
    """
    pass


class NotInDataBase(Exception):
    """
    Exception raised when an item is not found in the database.
    """
    pass


class GHParser:
    """
    The GHParser class provides static methods for parsing GitHub events and saving them to the database.

    Methods:
    - _process_event(event):
        Processes an individual GitHub event from the GitHub API response and extracts relevant information.
        Returns a tuple of (event type, repository ID, repository name, event datetime), or None if the event type
        is unrecognized.

    - parse(token: str):
        Parses GitHub events from the GitHub API, creates Event objects, and saves them to the database.

    Note: This class assumes the existence of appropriate database models (Repository, Event, EventType).
    Note: This class does not need to be instantiated, as all its methods are static.
    """

    @staticmethod
    def _process_event(event):
        """
        Processes an individual GitHub event from the GitHub API response.

        This method takes as input an event dictionary from the GitHub API, extracts relevant
        information (event type, repository ID, repository name, event datetime), and returns
        it in a tuple. If the event type is not recognized (i.e., it's not in the `EventTypes`
        enumeration), this method returns None.

        :param event: The GitHub API event dictionary.
        :return: A tuple of (event type, repository ID, repository name, event datetime),
                 or None if the event type is unrecognized.
        """
        try:
            event_type: EventTypes = EventTypes(event['type'])
        except ValueError:
            # Event that we do not want to collect information about
            # For example: `PushEvent`
            return None
        repo_id = event['repo']['id']
        repo_name = event['repo']['name']
        event_datetime = event['created_at']
        return event_type, repo_id, repo_name, event_datetime

    @staticmethod
    def parse(token: str):
        """
        Parses GitHub events from the GitHub API.

        This method makes a GET request to the GitHub API events endpoint, using the provided
        authentication token. It parses the returned data, creates Event objects for each
        recognized event type, and saves these to the database.

        :param token: The GitHub API token for authentication.
        :raises RateLimitExceededError: If the API rate limit has been exceeded.
        :return: None. All results are saved to the database.
        """
        response = requests.get('https://api.github.com/events', headers={'Authorization': token})
        if response.status_code == 429:
            raise RateLimitExceededError("We've crossed the limit of possible messages.\nUser access token "
                                         "requests are limited to 5,000 requests per hour.")
        data = json.loads(response.text)
        for event in data:
            processed = GHParser._process_event(event)
            if processed is None:
                continue

            event_type, repo_id, repo_name, event_datetime = processed

            repository, _ = Repository.objects.get_or_create(gh_repo_id=repo_id, defaults={'name': repo_name})
            event_type_instance, _ = EventType.objects.get_or_create(event_type=event_type.name)
            Event.objects.create(
                event_type=event_type_instance,
                repo=repository,
                created_at=timezone.now()
            )


class Analyzer:
    """
    The Analyzer class provides static(!) methods for analyzing events and calculating metrics.

    Methods:
    - get_average_pull_request(repository_id):
        Retrieves the average time between pull request events for a specific repository.

    Note: This class assumes the existence of appropriate database models (Repository, Event, EventType,
    PullRequestMetrics) and their relationships.
    Note: This class does not need to be instantiated, as all its methods are static.
    """

    @staticmethod
    def get_average_pull_request(repository_id: int):
        """
        Retrieves the average time between pull request events for a specific repository.

        This method calculates the average time between consecutive pull request events for the given repository.
        It returns the average time in the format 'X days, HH:MM:SS'.

        :param repository_id: The ID of the repository.
        :return: The average time between pull request events as a formatted string,
                 or an error message if the `repository`, `event`, or `event type` does not exist in the database.
        """
        try:
            repository = Analyzer.__get_repository(repository_id)
            event_type = Analyzer.__get_event_type('PullRequestEvent')
            events = Analyzer.__get_events(repository, event_type)
        except NotInDataBase as e:
            return e

        if len(events) < 2:
            # Difference between one(1)/zero(0) datetime(-s) is zero(0)
            Analyzer.__save_pull_request_metrics(repository, '0')
            return '0 days, 00:00:00'

        average_difference = Analyzer.__calculate_average_difference(events)
        formatted_average_difference = Analyzer.__format_timedelta(average_difference)

        Analyzer.__save_pull_request_metrics(repository, formatted_average_difference)

        return formatted_average_difference

    @staticmethod
    def __calculate_average_difference(events):
        """
        Calculates the average time difference between events.

        This method takes a list of events and calculates the average time difference between consecutive events.

        :param events: A list of events sorted by their creation date and time.
        :return: The average time difference between events as a timedelta object.
        """
        datetime_list = [event.created_at for event in events]

        # Convert the list into a NumPy array
        datetime_array = np.array(datetime_list)
        float_time_array = np.array([dt.timestamp() for dt in datetime_array])

        # Calculate the differences between each pair of consecutive times
        diffs = np.diff(float_time_array)
        average_diff = np.mean(diffs)

        # Convert the average difference from seconds to a timedelta object
        average_timedelta = timedelta(seconds=float(average_diff))
        return average_timedelta

    @staticmethod
    def __format_timedelta(timedelta_obj):
        """
        Formats a timedelta object into a string representation.

        This method takes a timedelta object and formats it into a string representation in the format
        'X days, HH:MM:SS'.

        :param timedelta_obj: The timedelta object to format.
        :return: The formatted string representation of the timedelta.
        """
        days = timedelta_obj.days
        hours, remainder = divmod(timedelta_obj.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{days} days, {hours:02}:{minutes:02}:{seconds:02}'

    @staticmethod
    def __get_repository(repository_id: int):
        """
        Retrieves a repository object from the database based on the repository ID.

        This method retrieves the repository object from the database that matches the provided repository ID.

        :param repository_id: The ID of the repository to retrieve.
        :raises NotInDataBase: If no repository with the provided ID exists in the database.
        :return: The repository object if found.
        """
        try:
            return Repository.objects.get(gh_repo_id=repository_id)
        except Repository.DoesNotExist:
            raise NotInDataBase('No existing repository')

    @staticmethod
    def __get_event_type(event_type_name: str):
        """
        Retrieves an event type object from the database based on the event type name.

        This method retrieves the event type object from the database that matches the provided event type name.

        :param event_type_name: The name of the event type to retrieve.
        :raises NotInDataBase: If no event type with the provided name exists in the database.
        :return: The event type object if found.
        """
        try:
            return EventType.objects.get(event_type=event_type_name)
        except EventType.DoesNotExist:
            raise NotInDataBase(f"No existing event type in database for '{event_type_name}'")

    @staticmethod
    def __get_events(repository, event_type):
        """
        Retrieves events for a specific repository and event type.

        This method retrieves all events from the database that are associated with
        the provided repository and event type.
        The events are ordered by their creation date and time.

        :param repository: The repository object for which to retrieve the events.
        :param event_type: The event type object for which to retrieve the events.
        :return: QuerySet containing the retrieved events.
        """
        return Event.objects.filter(repo=repository, event_type=event_type).order_by('created_at')

    @staticmethod
    def __save_pull_request_metrics(repository, average_difference_str):
        """
        Saves the pull request metrics to the database.

        This method creates a `PullRequestMetrics` instance with the provided repository and average difference string,
        and saves it to the database.

        :param repository: The repository object associated with the pull request metrics.
        :param average_difference_str: The average difference between pull request events as a formatted string.
        :return: None
        """
        PullRequestMetrics.objects.create(gh_repo_id=repository, respond=average_difference_str).save()

    @staticmethod
    def __merge_dictionaries(array_of_dicts):
        """
        Merges multiple dictionaries into one.

        This method takes as input a list of dictionaries, each of which contains the keys
        'event_type__event_type' and 'count'. It creates a new dictionary where each key is
        the value of 'event_type__event_type' and each value is the corresponding 'count'.

        :param array_of_dicts: List of dictionaries to be merged.
        :return: Merged dictionary where keys are event types and values are counts.
        """
        return {dictionary['event_type__event_type']: dictionary['count'] for dictionary in array_of_dicts}

    @staticmethod
    def get_number_of_events_groupped(offset):
        """
        Retrieves the number of events grouped by event type within a specified time offset.

        This method takes an offset parameter, which represents the number of minutes to consider
        for fetching the events. It retrieves the events that occurred within the time offset
        from the current datetime. It then calculates the count of each event type and returns
        a dictionary with event types as keys and their corresponding counts as values.

        :param offset: The time offset in minutes to consider for fetching the events.
        :return: A dictionary where keys are event types and values are the counts of events.
        """
        current_time = datetime.now()
        time_threshold = current_time - timedelta(minutes=offset)

        events = Event.objects.filter(created_at__lte=current_time, created_at__gte=time_threshold)
        event_counts = events.values('event_type__event_type').annotate(count=Count('event_type'))

        return Analyzer.__merge_dictionaries(event_counts)


class Visualizer:
    """
    The Visualizer class provides static(!) methods for creating visual representations of event metrics.

    Methods:
    - visualize_events_metrics:
        Creates a bar chart of event metrics for a specified time offset and returns it as a byte stream.

    Note: This class does not need to be instantiated, as all its methods are static.
    """

    @staticmethod
    def __summarize_values(data):
        """
        Private helper method to calculate the sum of values in the provided dictionary.

        :param data: Dictionary with the data to be summarized.
        :return: Sum of the dictionary values.
        """
        return sum(data.values())

    @staticmethod
    def visualize_events_metrics(offset: int):
        """
        Creates a bar chart visualization of events metrics and returns it as a byte stream.

        This method fetches the grouped events metrics for the specified offset (gap time) in
        minutes, generates a bar chart visualization of these metrics using matplotlib,
        and returns this chart as a byte stream in PNG format.

        :param offset: The gap time in minutes to consider for fetching the events metrics.
        :return: BytesIO stream representing the PNG image of the bar chart.
        """
        BAR_COLOR = "#2E6DFF"
        SUMMARIZED_COLOR = "#719DFF"
        data = Analyzer.get_number_of_events_groupped(offset)
        data['Summarized'] = Visualizer.__summarize_values(data)
        plt.title(f'Created events in last {offset} minute(-s)')

        names = list(data.keys())
        values = list(data.values())
        bars = plt.bar(range(len(data)), values, tick_label=names)

        # Set colors
        for bar in bars:
            bar.set_color(BAR_COLOR)
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center')
        bars[-1].set_color(SUMMARIZED_COLOR)
        # End

        # Send bytes of graph representation
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.clf()  # Clear current plot
        buf.seek(0)
        return buf
