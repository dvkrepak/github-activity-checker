from django.contrib import admin

from .models import Repository, Event, PullRequestMetrics


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'repo_id', 'events', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'repository_id', 'created_at', )


class PullRequestMetricsAdmin(admin.ModelAdmin):
    list_display = ('repository_id', 'respond', )


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PullRequestMetrics, PullRequestMetricsAdmin)
