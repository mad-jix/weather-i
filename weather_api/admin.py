from django.contrib import admin
from .models import Weather

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'timestamp')
    list_filter = ('city', 'timestamp')
    search_fields = ('city',)
    ordering = ('-timestamp',)
