from rest_framework import serializers
from .models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['id', 'city', 'temperature', 'timestamp']
        read_only_fields = ['timestamp'] 