from django.contrib import admin

from .models import Repository, Event, EventType, PullRequestMetrics


class RepositoryAdmin(admin.ModelAdmin):
    """
    Admin class for the Repository model.

    This class defines the admin interface configuration for the Repository model.

    Attributes:
    - list_display (tuple): The fields to be displayed in the admin list view.
    """
    list_display = ('id', 'name', 'gh_repo_id', )


class EventTypeAdmin(admin.ModelAdmin):
    """
    Admin class for the EventType model.

    This class defines the admin interface configuration for the EventType model.

    Attributes:
    - list_display (tuple): The fields to be displayed in the admin list view.
    """
    list_display = ('event_type', )


class EventAdmin(admin.ModelAdmin):
    """
    Admin class for the Event model.

    This class defines the admin interface configuration for the Event model.

    Attributes:
    - list_display (tuple): The fields to be displayed in the admin list view.
    """
    list_display = ('id', 'event_type', 'created_at', )


class PullRequestMetricsAdmin(admin.ModelAdmin):
    """
    Admin class for the PullRequestMetrics model.

    This class defines the admin interface configuration for the PullRequestMetrics model.

    Attributes:
    - list_display (tuple): The fields to be displayed in the admin list view.
    """
    list_display = ('gh_repo_id', 'respond', )


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PullRequestMetrics, PullRequestMetricsAdmin)
