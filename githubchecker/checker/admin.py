from django.contrib import admin

from .models import Repository, Event


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'repository_id', 'created_at', )


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Event, EventAdmin)
