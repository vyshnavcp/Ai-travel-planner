from django.shortcuts import render
import ollama
import markdown
from django.utils.safestring import mark_safe
# Create your views here.



def generate_itinerary(destination, budget, days, travel_type):

    prompt = f"""
You are a professional travel planner.

Destination: {destination}
Budget: ₹{budget}
Duration: {days} Days
Travel Type: {travel_type}

Create a detailed travel plan.

Include:

# Trip Overview

# Recommended Hotels
Mention at least 5 hotels with:
- Hotel Name
- Location
- Price Per Night

# Tourist Attractions

# Day Wise Itinerary

# Expense Breakdown
- Hotel Cost
- Food Cost
- Transportation Cost
- Attraction Cost

# Food Recommendations

# Travel Tips

Format response using proper headings and bullet points.
"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"# Error\n\n{str(e)}"


def travel_planner(request):

    result = None

    if request.method == "POST":

        destination = request.POST.get("destination")
        budget = request.POST.get("budget")
        days = request.POST.get("days")
        travel_type = request.POST.get("travel_type")

        ai_response = generate_itinerary(
            destination,
            budget,
            days,
            travel_type
        )

        result = mark_safe(
            markdown.markdown(ai_response)
        )

    return render(
        request,
        "travel_planner.html",
        {
            "result": result
        }
    )