from django.contrib import admin
from .models import Repository, Event, EventType, PullRequestMetrics


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gh_repo_id', )


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('event_type', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'created_at', )


class PullRequestMetricsAdmin(admin.ModelAdmin):
    list_display = ('gh_repo_id', 'respond', )


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PullRequestMetrics, PullRequestMetricsAdmin)
