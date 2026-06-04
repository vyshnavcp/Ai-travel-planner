from django.db import models

# Create your models here.

class TravelPlan(models.Model):
    destination = models.CharField(max_length=100)
    budget = models.IntegerField()
    days = models.IntegerField()
    itinerary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
