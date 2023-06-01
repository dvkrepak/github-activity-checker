from django.http import HttpResponse, JsonResponse

from .utils import Visualizer, Analyzer


def pull_request_metrics(request, repo: int):
    """
    API view for fetching pull request metrics for a specific repository.

    This view calculates the average time for 'PullRequestEvent' type events
    associated with the specified GitHub repository and returns it as a JSON response.

    :param request: The incoming HTTP request.
    :param repo: The ID of the GitHub repository for which to fetch metrics.
    :return: JsonResponse containing the 'github_repository_id' and 'average_time' for pull requests.
    """
    average_time = Analyzer.get_average_pull_request(repo)
    response_data = {
        'github_repository_id': repo,
        'average_time': average_time
    }
    return JsonResponse(response_data)


def events_metrics(request, offset: int):
    """
    API view for getting grouped event metrics.

    This view returns a JSON response containing the count of different event
    types created within the specified offset (gap time) in minutes.

    :param request: The incoming HTTP request.
    :param offset: The gap time in minutes to consider for fetching the events metrics.
    :return: JsonResponse containing the counts of different event types.
    """
    response_data = Analyzer.get_number_of_events_groupped(offset)
    return JsonResponse(response_data)


def events_metrics_visualization(request, offset: int):
    """
    API view for visualizing events metrics.

    This view generates a bar chart representing the number of different event
    types created within the specified offset (gap time) in minutes. The chart
    is returned as an image in PNG format.

    :param request: The incoming HTTP request.
    :param offset: The gap time in minutes to consider for generating the events metrics.
    :return: HttpResponse containing the generated PNG image of the bar chart.
    """

    buf = Visualizer.visualize_events_metrics(offset)
    return HttpResponse(buf, content_type='image/png')
