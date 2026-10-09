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
    sector_feeds = {
        "https://svt.se/rss.xml"
    }

    all_transmissions = []

    for url in sector_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                all_transmissions.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', 'Unknown Stardate'),
                    'summary': entry.get('summary', 'No further intel available.')
                })
        except Exception as e:
            print(f"Signal interference from {url}: {e}")

    return render(request, "dashboard/news.html", {"articles": all_transmissions[:10]})
