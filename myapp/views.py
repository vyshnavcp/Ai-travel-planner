from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.core.cache import cache
import ollama
import markdown
import hashlib


def build_prompt(destination, budget, days, travel_type):
    return f"""You are a travel planner. Create a {days}-day itinerary for {destination}.
Budget: ₹{budget} | Travel type: {travel_type}

Include:
# Trip Overview
# Hotels (3 options with name, location, price/night)
# Day-Wise Itinerary
# Expense Breakdown
# Food Tips
# Travel Tips

Use markdown headings and bullet points. Be concise."""


def generate_itinerary(destination, budget, days, travel_type):

    cache_key = hashlib.md5(
        f"{destination}{budget}{days}{travel_type}".encode()
    ).hexdigest()

    cached = cache.get(cache_key)
    if cached:
        return cached, True

    try:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": build_prompt(destination, budget, days, travel_type)
                }
            ]
        )
        result = response["message"]["content"]
        cache.set(cache_key, result, timeout=60 * 60 * 6)
        return result, False

    except Exception as e:
        return f"# Error\n\n{str(e)}", False


def stream_itinerary(destination, budget, days, travel_type):

    cache_key = hashlib.md5(
        f"{destination}{budget}{days}{travel_type}".encode()
    ).hexdigest()

    cached = cache.get(cache_key)

    if cached:
        html = markdown.markdown(cached)
        yield f"data:{html}\n\n"
        return

    full_response = ""

    try:
        for chunk in ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": build_prompt(destination, budget, days, travel_type)
                }
            ],
            stream=True
        ):
            token = chunk["message"]["content"]
            full_response += token
            yield f"data:{token}\n\n"

        cache.set(cache_key, full_response, timeout=60 * 60 * 6)

    except Exception as e:
        yield f"data:Error: {str(e)}\n\n"


def travel_planner(request):

    if request.method == "POST":
        destination = request.POST.get("destination", "").strip()
        budget = request.POST.get("budget", "").strip()
        days = request.POST.get("days", "").strip()
        travel_type = request.POST.get("travel_type", "").strip()

        if not all([destination, budget, days, travel_type]):
            return render(request, "travel_planner.html", {
                "error": "Please fill in all fields."
            })

        def event_stream():
            yield from stream_itinerary(destination, budget, days, travel_type)

        return StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream"
        )

    return render(request, "travel_planner.html", {})