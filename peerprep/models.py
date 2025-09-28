from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    experience_level = models.CharField(
        max_length=50,
        choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")],
        default="beginner"
    )

    def __str__(self):
        return self.user.username

class StudyNote(models.Model):
    SUBJECT_CHOICES = [
        ('cs', 'Computer Science'),
        ('math', 'Mathematics'),
        ('phy', 'Physics'),
        ('chem', 'Chemistry'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    file = models.FileField(upload_to="notes/")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def get_uploader_name(self):
        return self.uploader.get_full_name() or self.uploader.username

    def __str__(self):
        return self.title
    
class Question(models.Model):
    """Coding questions for practice"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=50,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        default="easy"
    )
    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class Session(models.Model):
    """Coding interview session between users"""
    participants = models.ManyToManyField(User, related_name="sessions")
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.id} - {self.question}"


class Message(models.Model):
    """Chat messages during a session"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.sender.username}: {self.content[:30]}"


class CodeSubmission(models.Model):
    """Stores code written during a session"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50, default="python")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username} in {self.language}"

class Note(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    file = models.FileField(upload_to='notes/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject}"