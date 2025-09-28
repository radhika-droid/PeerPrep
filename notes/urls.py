# notes/urls.py
from django.urls import path
from . import views

app_name = "notes"  

urlpatterns = [
    path("", views.notes_page, name="notes_page"),
]
