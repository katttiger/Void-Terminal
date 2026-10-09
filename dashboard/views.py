from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import psutil
import requests
import feedparser
# Create your views here.


def index(request):
    return render(request, "dashboard/index.html")


def sensor_data(request):
    net_counters = psutil.net_io_counters()
    data = {
        'cpu_usage': psutil.cpu_percent(),
        'ram_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'net_io_tx': net_counters.bytes_sent,  # Correct attribute name
        'net_io_rx': net_counters.bytes_recv,  # Correct attribute name
    }
    return JsonResponse(data)


def sensors(request):
    context = {
        'cpu_usage': psutil.cpu_percent(),
        'ram_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'net_io': psutil.net_io_counters(),
        'cpu_count': psutil.cpu_count(),
        # Convert to GB
        'ram_total': round(psutil.virtual_memory().total / (1024**3), 2),
    }
    return render(request, "dashboard/sensors.html", context)


def weather_report(request):
    city = "Stockholm"
    url = f"https://wttr.in/{city}?format=3"

    try:
        response = requests.get(url)
        weather_data = response.text
    except Exception as e:
        weather_data = {f'Unable to fetch weather data. Error: {e}'}

    return render(request, 'dashboard/weather.html', {'weather': weather_data, 'city': city})


def news_report(request):
    news_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    headlines = []

    try:
        feed = feedparser.parse(news_url)
        for entry in feed.entries[:5]:
            headlines.append({"title": entry.title, "link": entry.link})
    except Exception:
        headlines = [{"title": "News feed temporarily offline", "link": "#"}]

    return render(request, 'dashboard/news.html', {
        'news': headlines
    })
