from django.contrib import admin
from .models import Download

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'format', 'created_at')
    list_filter = ('format', 'created_at')
    search_fields = ('title', 'url')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
