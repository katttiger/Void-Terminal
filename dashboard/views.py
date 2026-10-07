from django.shortcuts import render
from django.http import HttpResponse
import psutil
# Create your views here.


def index(request):
    return render(request, "dashboard/index.html")


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
