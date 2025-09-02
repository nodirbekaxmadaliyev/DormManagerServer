# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("stream/", views.stream_webhook, name="stream_webhook"),
]
