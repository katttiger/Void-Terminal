from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("sensors/", views.sensors, name="sensors"),
    path("api/sensors/", views.sensor_data, name="sensor_data")
]
