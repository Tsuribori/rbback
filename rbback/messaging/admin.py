from django.contrib import admin
from messaging.models import Media, Thread, Message


class MediaAdmin(admin.ModelAdmin):
    search_fields = ['media_id']


admin.site.register(Media, MediaAdmin)
admin.site.register(Thread)
admin.site.register(Message)
