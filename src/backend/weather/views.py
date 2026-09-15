from django.shortcuts import render

# Create your views here.
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_live_weather(request):
    city = request.GET.get('city', 'Rajkot')  # Default city
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        res = requests.get(url).json()
        if res.get("cod") != 200:
            return Response({"error": res.get("message", "City not found")}, status=400)
            
        weather_data = {
            "city": res["name"],
            "temperature": res["main"]["temp"],
            "humidity": res["main"]["humidity"],
            "wind_speed": res["wind"]["speed"],
            "rainfall": res.get("rain", {}).get("1h", 0.0),
            "condition": res["weather"][0]["description"]
        }
        return Response(weather_data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)