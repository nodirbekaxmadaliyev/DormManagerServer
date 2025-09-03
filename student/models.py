from django.db import models
from django.utils import timezone

class Student(models.Model):
    student_id = models.IntegerField(blank= True, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    is_in_dormitory = models.BooleanField(default=False)
    parent_full_name = models.CharField(max_length=255, blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    checkout_time = models.DateTimeField(blank=True, null=True)
    sub_time = models.DateTimeField(default=timezone.now)
    chat_id = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
