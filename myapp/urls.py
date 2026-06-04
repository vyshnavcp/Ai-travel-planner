
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path("", views.travel_planner, name="travel_planner"),
    path('generate-itinerary/', views.travel_planner, name='generate_itinerary'),
   
]
