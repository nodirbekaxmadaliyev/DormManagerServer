from django.apps import AppConfig
import threading

class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "student"

