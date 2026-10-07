from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import psutil
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
