from django.contrib import admin
from .models import ShortURL

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'short_url', 'visits_count', 'created_at')
    search_fields = ('url', 'short_url')
    readonly_fields = ('visits_count', 'created_at')
