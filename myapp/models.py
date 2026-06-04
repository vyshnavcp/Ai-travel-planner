from django.db import models

# Create your models here.

class TravelPlan(models.Model):

    TRAVEL_TYPE_CHOICES = [
        ('Solo', 'Solo'),
        ('Couple', 'Couple'),
        ('Family', 'Family'),
        ('Friends', 'Friends'),
    ]
    destination = models.CharField(max_length=100)
    budget = models.IntegerField()
    days = models.IntegerField()
    travel_type = models.CharField(max_length=20, choices=TRAVEL_TYPE_CHOICES)
    itinerary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.destination} — {self.days} days ({self.travel_type})"