# notes/models.py
from django.db import models
from django.contrib.auth.models import User


class StudyNote(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('cs', 'Computer Science'),
        ('ds', 'Data Structures'),
        ('algorithms', 'Algorithms'),
        ('web', 'Web Development'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    file = models.FileField(upload_to='study_notes/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_uploader_name(self):
        user = self.uploader
        if user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        elif user.first_name:
            return user.first_name
        return user.username

class Note(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    file = models.FileField(upload_to='notes/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject}"
