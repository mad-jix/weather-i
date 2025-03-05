from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField(
        validators=[
            MinValueValidator(-100, message="Temperature cannot be less than -100°C"),
            MaxValueValidator(100, message="Temperature cannot be more than 100°C")
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Weather Records'
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['-timestamp']),
        ]
