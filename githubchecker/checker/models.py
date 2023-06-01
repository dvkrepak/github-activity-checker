from django.db import models

from .validators import validate_respond_structure


class Repository(models.Model):
    """
    Model class representing a GitHub repository.

    Fields:
    - name (CharField): The name of the repository.
    - gh_repo_id (BigIntegerField): The GitHub repository ID.

    Methods:
    - __str__(): Returns a string representation of the repository.

    Meta:
    - verbose_name: The human-readable singular name for the model.
    - verbose_name_plural: The human-readable plural name for the model.
    """
    name = models.CharField(max_length=255)
    gh_repo_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'


class EventType(models.Model):
    """
    Model class representing a GitHub event type.

    Fields:
    - event_type (CharField): The event type name.

    Methods:
    - __str__(): Returns a string representation of the event type.

    Meta:
    - verbose_name: The human-readable singular name for the model.
    - verbose_name_plural: The human-readable plural name for the model.
    """
    event_type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.event_type

    class Meta:
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'


class Event(models.Model):
    """
    Model class representing GitHub events.

    Fields:
    - event_type (ForeignKey): The foreign key reference to the EventType model.
    - repo (ForeignKey): The foreign key reference to the Repository model.
    - created_at (DateTimeField): The timestamp when the event was created.

    Methods:
    - __str__(): Returns a string representation of the event.

    Meta:
    - verbose_name: The human-readable singular name for the model.
    - verbose_name_plural: The human-readable plural name for the model.
    """
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
    repo = models.ForeignKey(Repository, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.event_type} at {self.created_at}'

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class PullRequestMetrics(models.Model):
    """
    Model class representing pull request metrics.

    Fields:
    - gh_repo_id (ForeignKey): The foreign key reference to the Repository model.
    - respond (CharField): The response time in the format "<int> days, <int:2>:<int:2>:<int:2>".

    Methods:
    - __str__(): Returns a string representation of the pull request metric.

    Meta:
    - verbose_name: The human-readable singular name for the model.
    - verbose_name_plural: The human-readable plural name for the model.
    """
    gh_repo_id = models.ForeignKey('Repository', on_delete=models.PROTECT)
    respond = models.CharField(
        max_length=50,
        default=None,
        validators=[validate_respond_structure],
        help_text='The response time in the format "<int> days, <int:2>:<int:2>:<int:2>".'
    )

    def __str__(self):
        return f'Pull request metric about repo {self.gh_repo_id} = {self.respond}'

    class Meta:
        verbose_name = 'Pull Request Metric'
        verbose_name_plural = 'Pull Request Metrics'
