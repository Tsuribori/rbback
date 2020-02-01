from django.contrib import admin
from messaging.models import Media, Thread, Message


class MediaAdmin(admin.ModelAdmin):
    search_fields = ['media_id']


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['subject', 'public']
    actions = ['hide_thread']

    def hide_thread(self, request, queryset):
        queryset.update(public=False)

    hide_thread.short_description = "Hide selected threads"


admin.site.register(Media, MediaAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message)
