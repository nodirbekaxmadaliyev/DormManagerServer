from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_student, name="add-student"),
    path("update/<int:pk>/", views.update_student, name="update-student"),
    path("delete/", views.delete_student, name="delete-student"),
]
