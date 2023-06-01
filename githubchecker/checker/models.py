from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=255)
    gh_repo_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'


class EventType(models.Model):
    event_type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.event_type

    class Meta:
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'


class Event(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    repo = models.ForeignKey(Repository, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.event_type} at {self.created_at}'

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class BasicMetrics(models.Model):
    gh_repo_id = models.ForeignKey(Repository, on_delete=models.PROTECT)

    def __str__(self):
        return 'Basic metric'

    class Meta:
        verbose_name = 'Basic Metric'
        verbose_name_plural = 'Basic Metrics'


class PullRequestMetrics(BasicMetrics):
    # Char representation of date
    # For example: `0 days, 02:01:18`
    respond = models.CharField(max_length=50, default=None)

    def __str__(self):
        return f'Pull request metric about repo {self.gh_repo_id} = {self.respond}'

    class Meta:
        verbose_name = 'Pull Request Metric'
        verbose_name_plural = 'Pull Request Metrics'
