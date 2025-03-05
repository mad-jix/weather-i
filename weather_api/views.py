from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.conf import settings
from .models import Weather
from .serializers import WeatherSerializer
from datetime import datetime

# Create your views here.

class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    @action(detail=False, methods=['post'])
    def fetch_weather(self, request):
        """
        Fetch current weather and 5-day forecast from OpenWeatherMap API
        """
        city = request.data.get('city')
        if not city:
            return Response(
                {'error': 'City name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # OpenWeatherMap API configuration
            api_key = settings.WEATHER_API_KEY
            
            # Get current weather
            current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
            current_params = {
                'q': city,
                'appid': api_key,
                'units': 'metric',
                'lang': 'en'
            }
            
            current_response = requests.get(current_weather_url, params=current_params)
            
            # Get 5-day forecast
            forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
            forecast_params = {
                'q': city,
                'appid': api_key,
                'units': 'metric',
                'lang': 'en'
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params)
            
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                current_data = current_response.json()
                forecast_data = forecast_response.json()
                
                # Process forecast data to get daily forecasts
                daily_forecasts = []
                seen_dates = set()
                
                for item in forecast_data['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in seen_dates:
                        seen_dates.add(date)
                        daily_forecasts.append({
                            'date': date,
                            'temperature': round(item['main']['temp'], 1),
                            'description': item['weather'][0]['description'],
                            'icon': item['weather'][0]['icon']
                        })
                        if len(daily_forecasts) >= 5:  # Limit to 5 days
                            break
                
                # Create weather record for current weather
                weather_data = {
                    'city': city,
                    'temperature': round(current_data['main']['temp'], 1)
                }
                
                weather = Weather.objects.create(**weather_data)
                current_weather = self.get_serializer(weather).data
                
                # Add forecast data to response
                response_data = {
                    'current': {
                        'city': city,
                        'temperature': round(current_data['main']['temp'], 1),
                        'description': current_data['weather'][0]['description'],
                        'icon': current_data['weather'][0]['icon'],
                        'timestamp': datetime.now().isoformat(),
                        'humidity': current_data['main']['humidity'],
                        'pressure': current_data['main']['pressure'],
                        'visibility': current_data.get('visibility', 0),
                        'wind_speed': round(current_data['wind']['speed'], 1),
                        'feels_like': round(current_data['main']['feels_like'], 1)
                    },
                    'forecast': daily_forecasts
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            elif current_response.status_code == 404 or forecast_response.status_code == 404:
                return Response(
                    {'error': 'City not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            elif current_response.status_code == 401 or forecast_response.status_code == 401:
                return Response(
                    {'error': 'Invalid API key'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return Response(
                    {'error': f'OpenWeatherMap API error: {current_response.json().get("message", "Unknown error")}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Network error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {'error': f'Server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
