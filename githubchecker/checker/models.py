from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=255, default=None)
    repo_id = models.BigIntegerField(unique=True, default=None)
    events = models.ForeignKey('Event', on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'


class Event(models.Model):
    # Possible events
    WATCH_EVENT = 'WatchEvent'
    PULL_REQUEST_EVENT = 'PullRequestEvent'
    ISSUES_EVENT = 'IssuesEvent'
    # End

    EVENT_CHOICES = [
        (WATCH_EVENT, 'WatchEvent'),
        (PULL_REQUEST_EVENT, 'PullRequestEvent'),
        (ISSUES_EVENT, 'IssuesEvent')
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.event_type} in repository n.{self.repository_id}'

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class BasicMetrics(models.Model):
    repository_id = models.ForeignKey(Repository, on_delete=models.PROTECT, null=False, default=None)

    def __str__(self):
        return 'Basic metric'

    class Meta:
        verbose_name = 'Basic Metric'
        verbose_name_plural = 'Basic Metrics'


class PullRequestMetrics(BasicMetrics):
    respond = models.FloatField(default=None)

    def __str__(self):
        return f'Pull request metric about repo n.{self.repository_id} = {self.respond}'

    class Meta:
        verbose_name = 'Pull Request Metric'
        verbose_name_plural = 'Pull Request Metrics'
