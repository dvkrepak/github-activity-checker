from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=255)

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

    repository_id = models.ForeignKey(Repository, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
